from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import CustomizeInsights
from .serializers import CustomizeInsightsSerializer


class CustomizeInsightsSerializerTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )

        # Ensure the user has a CustomizeInsights instance
        CustomizeInsights.objects.create(user=self.user)

        # Create an API client
        self.client = APIClient()

    def test_valid_data(self):
        # Create a new user for this test
        new_user = get_user_model().objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='newpassword',
            first_name='Jane',
            last_name='Doe',
        )

        # Test valid data
        insights_data = {
            'user': new_user.id,
            'finance': True,
            'healthcare': False,
            'technology': True,
            'refresh_frequency': 'weekly',
        }

        serializer = CustomizeInsightsSerializer(data=insights_data)

        # Check if the serializer is valid
        if not serializer.is_valid():
            # Print serializer errors for debugging
            print(serializer.errors)

        # Assert that the serializer is valid
        self.assertTrue(serializer.is_valid())
