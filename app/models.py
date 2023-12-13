from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django_countries.fields import CountryField


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Assuming your user model has 'first_name', 'last_name', 'password' fields
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    country = CountryField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    profile_photo = models.ImageField(upload_to='profile-photos/', default=None, null=True, blank=True)

    def _create_user(self, email, username, first_name, last_name, password=None, gender=None,):
        """
        Creates and saves a User with the given email, username, password, gender, first_name, and last_name.
        """

        if not email:
            raise ValueError("Please enter your Email ID")

        email = self.normalize_email(email)

        with transaction.atomic(using=self._db):
            user = self.model(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            if password is not None:
                user.set_password(password)
            else:
                user.set_unusable_password()

        return user

    def create_superuser(self, username, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self._create_user(email, username, password, first_name=first_name, last_name=last_name, **extra_fields)


class RequestDemo(models.Model):
    Full_name = models.CharField(max_length=100)
    Company = models.CharField(max_length=100)
    Business_email = models.EmailField()
    # Country = CountryField()
    Contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.Full_name


class ContactUs(models.Model):
    Full_name = models.CharField(max_length=100)
    Company = models.CharField(max_length=100)
    Business_email = models.EmailField()
    # Country = CountryField()
    Contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.Full_name


class HelpandSupport(models.Model):
    Full_name = models.CharField(max_length=100)
    Company = models.CharField(max_length=100)
    Business_email = models.EmailField()
    # Country = CountryField()
    Contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.Full_name


# class SignupRequests(models.Model):
#
#     first_name = models.CharField(max_length=255, validators=[MinLengthValidator(limit_value=3)])
#     last_name = models.CharField(max_length=255, validators=[MinLengthValidator(limit_value=3)])
#     business_email = models.EmailField(unique= True, validators=[EmailValidator()])
#     country = CountryField()
#     contact_number = models.CharField(max_length=15, validators=[MinLengthValidator(limit_value=10),
#                                                                  RegexValidator(r'^[0-9]*$',
#                                                                                 'Contact number must contain only numeric characters.')])
#
#     def __str__(self):
#         return f"{self.title} {self.first_name} {self.last_name}"




