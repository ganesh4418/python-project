from django.db.models import Sum
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from axes.models import AccessAttempt
from axes.attempts import get_cool_off_threshold
from django_otp.plugins.otp_totp.models import TOTPDevice
from .models import CustomUser, RequestDemo, HelpandSupport, ContactUs
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django_countries.serializer_fields import CountryField
import re
import os


User = get_user_model()


class TwoFactorJwtTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Check if the user has two-factor authentication enabled
        user = self.user
        # if not user.two_factor_enabled:
        #     return data  # Return data as-is if 2FA is not enabled for this user

        # Generate a new access token without the refresh token claim
        refresh = self.get_token(user)
        data['access'] = str(refresh.access_token)

        # Generate a one-time password (OTP) for two-factor authentication
        otp_device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
        if otp_device:
            otp = otp_device.generate_otp()
            data['otp'] = otp

        return data


class CustomTokenObtainPairSerializer(TwoFactorJwtTokenObtainPairSerializer):
    default_error_messages = {"no_active_account": (
        "Login failed. Please check your username or email and password. Note that the password is case-sensitive.")}
    """
    This serves various purposes:
    1. It extends the default TokenObtainPairSerializer2FA to handle 2FA
    2. It adds to add the user's details to the response, saving an additional request after login.
    """

    def check_login_attempt(self, validate_data):
        login_failures_count = (
            AccessAttempt.objects.filter(username=validate_data.get("username"),
                                         attempt_time__gte=get_cool_off_threshold())
            .order_by("username")
            .values("username")
            .annotate(login_failures_count=Sum("failures_since_start"))
            .values("login_failures_count")
        )
        if len(login_failures_count) == 0:
            login_failures_count = 0
        else:
            login_failures_count = login_failures_count[0]['login_failures_count']
        if login_failures_count == 1:
            self.error_messages['no_active_account'] = (
                "1 failed login attempt: Your account will be locked out for 15 minutes after 1 more failure."
            )
        elif login_failures_count >= 2:
            self.error_messages['no_active_account'] = (
                "Your account is locked due to repeated login failures."
            )

    def validate(self, attrs):
        self.check_login_attempt(attrs)
        data = super().validate(attrs)

        # Add user details to response
        data["user"] = UserSerializer(self.user).data

        return data


class BaseUserSerializer(serializers.ModelSerializer):
    """Base serializer for User model"""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        depth = 1
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "country",
            "contact_number",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "user_permissions",
        )
        read_only_fields = (
            "id",
            "updated_by",
            "last_login",
            "is_superuser",
            "is_staff",
            "date_joined",
            "created",
            "modified",
            "user_permissions",
            "intercom_id",
            "parent",
        )

    def validate_email(self, value):
        # Check if the email is already in use
        user_query = User.objects.filter(email=value)
        if hasattr(self, "instance") and self.instance and self.instance.pk:
            user_query = user_query.exclude(pk=self.instance.pk)
        if user_query.exists():
            raise serializers.ValidationError("Email already exists")

        try:
            # Validate the email format
            serializers.EmailField().run_validation(value)
        except serializers.ValidationError as e:
            raise serializers.ValidationError("Please enter a valid email address.")

        # Extract domain from the email
        _, domain = value.split('@', 1)

        # Check if the domain is in the disallowed list
        disallowed_domains = ['gmail.com', 'yahoo.com', 'rediffmail.com', 'outlook.com', 'hotmail.com']
        if domain.lower() in disallowed_domains:
            raise serializers.ValidationError("Please use a corporate email address.")

        # Additional validation for the pattern
        if not re.match("^[a-zA-Z]+[a-zA-Z0-9_@.]*$", value):
            raise serializers.ValidationError("Please enter valid email id")

        # Check if the TLD is in the allowed list
        allowed_tlds = [
            ".us", ".uk", ".in", ".au", ".ca", ".de", ".fr", ".jp", ".cn", ".br",
            ".ru", ".mx", ".za", ".ae", ".sg",
            ".com", ".org", ".net", ".gov", ".edu", ".mil", ".int", ".co", ".info",
            ".biz", ".museum", ".name", ".pro", ".aero", ".coop", ".mobi", ".asia",
            ".jobs", ".tel"
        ]
        if not any(domain.lower().endswith(tld) for tld in allowed_tlds):
            raise serializers.ValidationError("Please enter valid email id")

        return value

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data.get("password", None)
        if password is None:
            user.set_unusable_password()
        else:
            user.set_password(password)
        user.save()

        return user


class UserSignupSerializer(BaseUserSerializer):
    class Meta:
        model = CustomUser
        fields = [field.name for field in model._meta.fields]

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        country = data.get('country')
        contact_number = data.get('contact_number')

        if email and username and email != username:
            raise serializers.ValidationError("Email and username must have the same value.")

        if not re.match("^[a-zA-Z0-9_@.]*$", email):
            raise serializers.ValidationError("Email can only contain alphabets, numbers, underscores, '@', and '.'.")

        if not re.match("^[a-zA-Z]*$", first_name):
            raise serializers.ValidationError("First name should only contain alphabetic characters.")

        if not re.match("^[a-zA-Z]*$", last_name):
            raise serializers.ValidationError("Last name should only contain alphabetic characters.")

        if first_name and (first_name.startswith(' ') or first_name.endswith(' ')):
            raise serializers.ValidationError("First name should not start or end with a space.")

        if last_name and (last_name.startswith(' ') or last_name.endswith(' ')):
            raise serializers.ValidationError("Last name should not start or end with a space.")

        cleaned_contact_number = ''.join(filter(str.isdigit, contact_number))  # Remove non-digit characters
        if not re.match(r'^\+?\d{6,16}$', cleaned_contact_number):
            raise serializers.ValidationError("Please enter a valid contact number with or without a country code.")

        if not re.match(r'^\d+$', contact_number):
            raise serializers.ValidationError("Please enter a valid contact number.")

        return data

    def validate_password(self, value):
        """
        Validate the password format.
        """
        # Password should contain minimum 8 and maximum 16 characters,
        # at least one uppercase, at least one special character, and at least one number.
        error_msg = "Password should contain minimum 8 and maximum 16 characters, one uppercase letter, one special character, and one number."
        if not (8 <= len(value) <= 16):
            raise serializers.ValidationError(error_msg)

        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(error_msg)

        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(error_msg)

        if not any(char in r"@#$%^&+=!" for char in value):
            raise serializers.ValidationError(error_msg)

        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(BaseUserSerializer):
    """
    General user serializer
    """

    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Group.objects.all(),
        allow_empty=False,
        required=False,
    )

    class Meta:
        model = BaseUserSerializer.Meta.model
        depth = BaseUserSerializer.Meta.depth
        fields = BaseUserSerializer.Meta.fields + ("groups",)
        read_only_fields = BaseUserSerializer.Meta.read_only_fields

    def validate(self, data):
        # We must have a user
        try:
            user = self.context["request"].user
            if not user or not user.is_authenticated:
                raise serializers.ValidationError("User must be authenticated to update a user.")
        except KeyError:
            raise serializers.ValidationError("User must be authenticated to update a user.")

        return super().validate(data)


class BaseSerializer(serializers.Serializer):
    Full_name = serializers.CharField()
    Company = serializers.CharField()
    Business_email = serializers.EmailField()
    Contact_number = serializers.CharField()

    def validate_Full_name(self, value):
        # Remove spaces and check if the remaining characters are at least 3
        if len(re.sub(r'\s', '', value)) < 3:
            raise serializers.ValidationError(
                "Full name should have at least 3 characters")

        # Check if the full name contains only letters and spaces
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError(
                "Full name should contain only letters.")

        return value

    def validate_Contact_number(self, value):
        cleaned_value = ''.join(filter(str.isdigit, value))
        if not (6 <= len(cleaned_value) <= 16):
            raise serializers.ValidationError("Please enter a valid contact_number.")
        return value

    def validate_Company(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Company name must be at least 3 characters long.")
        return value

    def validate_Business_email(self, value):
        try:
            serializers.EmailField().run_validation(value)
        except serializers.ValidationError as e:
            raise serializers.ValidationError("Please enter a valid email address.")

        _, domain = value.split('@', 1)
        disallowed_domains = ['gmail.com', 'yahoo.com', 'rediffmail.com', 'outlook.com', 'hotmail.com']

        # Check if the domain is in the disallowed list
        if domain.lower() in disallowed_domains:
            raise serializers.ValidationError("Please use a corporate email address.")

        # Additional validation for the pattern
        if not re.match("^[a-zA-Z]+[a-zA-Z0-9_@.]*$", value):
            raise serializers.ValidationError("Please enter valid email id")

        # Check if the TLD is in the allowed list
        allowed_tlds = [
            ".us", ".uk", ".in", ".au", ".ca", ".de", ".fr", ".jp", ".cn", ".br",
            ".ru", ".mx", ".za", ".ae", ".sg",
            ".com", ".org", ".net", ".gov", ".edu", ".mil", ".int", ".co", ".info",
            ".biz", ".museum", ".name", ".pro", ".aero", ".coop", ".mobi", ".asia",
            ".jobs", ".tel"
        ]
        if not any(domain.lower().endswith(tld) for tld in allowed_tlds):
            raise serializers.ValidationError("Please enter valid email id")

        return value

    def create(self, validated_data):
        # This method should not be used to create instances directly; it should be overridden in subclasses
        raise NotImplementedError("create method should be implemented in subclasses.")


class RequestDemoSerializer(BaseSerializer):
    def create(self, validated_data):
        # Create an instance of the RequestDemo model with the provided data
        return RequestDemo.objects.create(**validated_data)


class ContactUsSerializer(BaseSerializer):
    def create(self, validated_data):
        # Create an instance of the ContactUs model with the provided data
        return ContactUs.objects.create(**validated_data)


class HelpandSupportSerializer(BaseSerializer):
    def create(self, validated_data):
        # Create an instance of the HelpandSupport model with the provided data
        return HelpandSupport.objects.create(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField()
    photo_size = serializers.SerializerMethodField()
    photo_type = serializers.SerializerMethodField()
    photo_path = serializers.SerializerMethodField()

    def validate_profile_photo(self, value):
        if not value:
            response_data = {
                "error": True,
                "message": "Please select a profile photo."
            }
            raise ValidationError(response_data, code=status.HTTP_400_BAD_REQUEST)

        if value:
            file_extension = value.name.split('.')[-1].lower()
            allowed_formats = ['jpeg', 'jpg', 'png', 'gif']

            if file_extension not in allowed_formats:
                raise ValidationError("Please select an image file (JPEG, JPG, PNG, GIF).")
        return value

    def get_photo_size(self, obj):
        if obj.profile_photo:
            file_path = obj.profile_photo.path
            if os.path.exists(file_path):
                size_in_bytes = os.path.getsize(file_path)
                return size_in_bytes
        return None

    def get_photo_type(self, obj):
        if obj.profile_photo:
            return obj.profile_photo.name.split('.')[-1].lower()
        return None

    def get_photo_path(self, obj):
        if obj.profile_photo:
            return obj.profile_photo.url
        return None

    class Meta:
        model = CustomUser
        fields = ['profile_photo', 'photo_size', 'photo_type', 'photo_path']


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
