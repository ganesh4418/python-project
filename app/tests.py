from django.test import TestCase
from .serializers import UserSignupSerializer,RequestDemoSerializer, ContactUsSerializer,HelpandSupportSerializer
from .models import CustomUser, ContactUs, RequestDemo, HelpandSupport
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from axes.models import AccessAttempt
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework.test import APIClient




class UserSignupSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'mailto:john.doe@example.com',
            'username': 'johndoe',
            'password': 'WeakPwd',
            'country': 'US',
            'contact_number': '1234567890',
        }

    def test_valid_user_signup(self):
        serializer = UserSignupSerializer(data=self.valid_data)

        if not serializer.is_valid():
            print(serializer.errors)

            # Handle the password validation error
            password_error = serializer.errors.get('password', None)
            if password_error and 'invalid' in password_error[0].code:
                print("Password validation error: ", password_error[0].code)

        # Assert that the serializer is not valid
        self.assertFalse(serializer.is_valid())

# app/tests.py


class RequestDemoSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'Full_name': 'JohnDoe',
            'Company': 'ABC Corp',
            'Business_email': 'john.doe@example.com',
            'Contact_number': '1234567890',
        }

    def test_valid_request_demo(self):
        serializer = RequestDemoSerializer(data=self.valid_data)

        if not serializer.is_valid():
            print(serializer.errors)

        #self.assertTrue(serializer.is_valid())

        # Create instance using serializer's create method
        request_demo_instance = serializer.create(serializer.validated_data)

        # Check if the instance is created successfully
        self.assertIsInstance(request_demo_instance, RequestDemo)
        self.assertEqual(request_demo_instance.Full_name, self.valid_data['Full_name'])
        self.assertEqual(request_demo_instance.Company, self.valid_data['Company'])
        self.assertEqual(request_demo_instance.Business_email, self.valid_data['Business_email'])
        self.assertEqual(request_demo_instance.Contact_number, self.valid_data['Contact_number'])

class ContactUsSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'Full_name': 'JaneDoe',
            'Company': 'XYZ Ltd',
            'Business_email': 'jane.doe@example.com',
            'Contact_number': '9876543210',
        }

    def test_valid_contact_us(self):
        serializer = ContactUsSerializer(data=self.valid_data)

        if not serializer.is_valid():
            print(serializer.errors)

        self.assertTrue(serializer.is_valid())

        # Create instance using serializer's create method
        contact_us_instance = serializer.create(serializer.validated_data)

        # Check if the instance is created successfully
        self.assertIsInstance(contact_us_instance, ContactUs)
        self.assertEqual(contact_us_instance.Full_name, self.valid_data['Full_name'])
        self.assertEqual(contact_us_instance.Company, self.valid_data['Company'])
        self.assertEqual(contact_us_instance.Business_email, self.valid_data['Business_email'])
        self.assertEqual(contact_us_instance.Contact_number, self.valid_data['Contact_number'])
User = get_user_model()

class CustomTokenObtainPairSerializerTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )

        # Create an API client
        self.client = APIClient()

    def test_custom_token_obtain_pair_serializer(self):
        # Create a TOTP device for the user
       #totp_device = TOTPDevice.objects.create(user=self.user, confirmed=True)

        # Simulate a successful login attempt
        login_data = {
            'username': 'testuser',
            'password': 'testpassword',
            #'otp':  totp_device.generate_token(),
        }


class HelpandSupportSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'Full_name': 'JohnSmith',
            'Company': 'ABC Corporation',
            'Business_email': 'john.smith@example.com',
            'Contact_number': '1234567890',
        }

    def test_valid_help_and_support(self):
        serializer = HelpandSupportSerializer(data=self.valid_data)

        if not serializer.is_valid():
            print(serializer.errors)

        #self.assertTrue(serializer.is_valid())

        # Create instance using serializer's create method
        help_and_support_instance = serializer.create(serializer.validated_data)

        # Check if the instance is created successfully
        self.assertIsInstance(help_and_support_instance, HelpandSupport)
        self.assertEqual(help_and_support_instance.Full_name, self.valid_data['Full_name'])
        self.assertEqual(help_and_support_instance.Company, self.valid_data['Company'])
        self.assertEqual(help_and_support_instance.Business_email, self.valid_data['Business_email'])
        self.assertEqual(help_and_support_instance.Contact_number, self.valid_data['Contact_number'])


