from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Contact

class ContactAPITest(TestCase):
    """Test suite for the Contact API."""

    def setUp(self):
        """Set up the test client."""
        self.client = APIClient()

    def test_create_contact_valid_email(self):
        """Test creating a contact with a valid email."""
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'Hello!'
        }
        response = self.client.post('/api/contact/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().name, 'Jane Doe')

    def test_create_contact_invalid_email(self):
        """Test creating a contact with an invalid email."""
        data = {
            'name': 'John Doe',
            'email': 'johninvalid.com',
            'message': 'Hi!'
        }
        response = self.client.post('/api/contact/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Contact.objects.count(), 0)
