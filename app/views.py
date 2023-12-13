import jwt
import re
from rest_framework.views import APIView
from django.contrib.auth import logout
from rest_framework import generics
from .serializers import (UserSignupSerializer, ForgotPasswordSerializer,
                          ContactUsSerializer, HelpandSupportSerializer, RequestDemoSerializer, UserProfileSerializer)
from .models import CustomUser, ContactUs, RequestDemo, HelpandSupport
from rest_framework import viewsets, status
from .utils import send_verification_email, ForgotPassword_verification_email
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser

class UserSignupViewSet(APIView):
    """
    User Signup
    """
    serializer_class = UserSignupSerializer
    queryset = CustomUser.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Valid data, create a new user
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    """
    Extends the default TokenObtainPairView to add the user's details to the response,
    saving an additional request after login.
    """

    def post(self, request, *args, **kwargs):
        # Extract the username and password from the request data
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        # Validate the password format
        if not self.is_valid_password(password):
            return Response({
                'message': 'Password should contain minimum 8 and maximum 16 characters, '
                           'one uppercase, one special character, and one number.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Continue with the rest of the authentication logic
        serializer = self.serializer_class(data=request.data, context={'request': request})

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            # Handle the case where the username and password do not match or there are other validation errors
            return Response({
                                'message': 'Login failed. Please check your username or email and password. Note that the password is case-sensitive.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data['user']
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            token_exp = timezone.now() + timezone.timedelta(minutes=10)
            session_id = jwt.encode({'user_id': user.id, 'exp': int(token_exp.timestamp())}, 'your_secret_key',
                                    algorithm='HS256')
            user.last_login = timezone.now()
            user.save()

            response_data = {
                'token': token.key,
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'last_login': user.last_login.strftime("%Y-%m-%d %H:%M:%S"),
                'session_id': session_id,
                'token_expiration': token_exp.strftime("%Y-%m-%d %H:%M:%S"),
            }

            # Set session ID in a cookie with expiration time
            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie('session_id', session_id, expires=token_exp, secure=True, httponly=True)

            return response
        else:
            return Response({'message': 'User is inactive'}, status=status.HTTP_403_FORBIDDEN)

    def is_valid_password(self, password):
        """
        Validate the password format.
        """
        # Password should contain minimum 8 and maximum 16 characters,
        # at least one uppercase, at least one special character, and at least one number.
        if not (8 <= len(password) <= 16):
            return False

        if not any(char.isupper() for char in password):
            return False

        if not any(char.isdigit() for char in password):
            return False

        if not any(char in r"@#$%^&+=!" for char in password):
            return False

        return True

@api_view(['POST'])
def custom_logout(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class RequestDemoViewSet(viewsets.ModelViewSet):
    queryset = RequestDemo.objects.all()
    serializer_class = RequestDemoSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()

        # Send a verification email
        send_verification_email(submission, request_type='request demo')

        return Response(
            {"message": " Your Request for demo successfully registered"},
            status=status.HTTP_201_CREATED
        )

        def create(self, validated_data):
            return RequestDemo.objects.create(**validated_data)


class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()

        # Send a verification email
        send_verification_email(submission, request_type='contact')

        response_message = "Contact Us: Request sent successfully"
        return Response(
            {"message": response_message},
            status=status.HTTP_201_CREATED
        )


class HelpandSupportViewSet(viewsets.ModelViewSet):
    queryset = HelpandSupport.objects.all()
    serializer_class = HelpandSupportSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()

        # Send a verification email
        send_verification_email(submission, request_type='helpandsupport')

        response_message = "Help and Support: Request sent successfully"
        return Response(
            {"message": response_message},
            status=status.HTTP_201_CREATED
        )


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        # Check if the user making the request is the owner of the profile
        if request.user != instance:
            return Response({"message": "You do not have permission to update this profile."},
                            status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "profile photo updated Successfully",
                "data": serializer.data  # Include serialized data in the response
            },status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #
    #     # Check if the user making the request is the owner of the profile
    #     if request.user != instance:
    #         return Response({"message": "You do not have permission to update this profile."},
    #                         status=status.HTTP_403_FORBIDDEN)
    #
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "Profile photo updated successfully"}, status=status.HTTP_200_OK)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Check if email field is present in the request data
        if 'email' not in request.data:
            raise serializers.ValidationError("Enter your registered email id.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Check if the email is associated with a user
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User with this email is not registered.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            ForgotPassword_verification_email(email, request_type='ForgotPassword')
            return Response({'detail': 'Forgot password mail sent successfully.'}, status=status.HTTP_200_OK)