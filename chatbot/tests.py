from rest_framework.test import APIClient  # Use APIClient instead of Client
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from django.test import TestCase

class ChatbotTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.chat_url = reverse('chatbot')

    def test_chatbot_valid_message(self):
        """Test that a valid message receives a response."""
        response = self.client.post(self.chat_url, {'message': 'Tell me about the projects.'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.json())

    def test_chatbot_empty_message(self):
        """Test that an empty message returns a 400 error."""
        response = self.client.post(self.chat_url, {'message': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'Please enter a message to get a response.')

    def test_chatbot_rate_limit(self):
        """Test that rate limiting works after 5 requests in a minute."""
        for _ in range(5):
            self.client.post(self.chat_url, {'message': 'Test'}, format='json')
        response = self.client.post(self.chat_url, {'message': 'Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    @patch('openai.Completion.create')
    def test_chatbot_openai_mock(self, mock_openai):
        """Test that the chatbot returns a mocked OpenAI response."""
        mock_openai.return_value = {'choices': [{'text': 'Mock response'}]}
        response = self.client.post(self.chat_url, {'message': 'Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Mock response')

    def test_cached_response(self):
        """Same message should return a cached response."""
        response1 = self.client.post(self.chat_url, {'message': 'Tell me about the projects.'}, format='json')
        response2 = self.client.post(self.chat_url, {'message': 'Tell me about the projects.'}, format='json')
        self.assertEqual(response1.json(), response2.json())
