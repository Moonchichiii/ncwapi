from rest_framework.test import APIClient, override_settings
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from django.middleware.csrf import get_token
from django.test import override_settings

@override_settings(CSRF_MIDDLEWARE=False)
class ChatbotTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.chat_url = reverse('chatbot')

    def test_chatbot_valid_message(self):
        """Test chatbot with a valid message."""
        response = self.client.post(
            self.chat_url, 
            {'message': 'Tell me about the projects.'}, 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.json())

    def test_chatbot_empty_message(self):
        """Test chatbot with an empty message."""
        response = self.client.post(
            self.chat_url, 
            {'message': ''}, 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'Please enter a message to get a response.')

    @patch('openai.Completion.create')
    def test_chatbot_openai_mock(self, mock_openai):
        """Test chatbot with a mocked OpenAI response."""
        mock_openai.return_value = {'choices': [{'text': 'Mock response'}]}
        response = self.client.post(
            self.chat_url, 
            {'message': 'Test'}, 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Mock response')

    @override_settings(RATELIMIT_ENABLE=False)
    def test_chatbot_rate_limit(self):
        """Test chatbot rate limiting."""
        for _ in range(5):
            self.client.post(self.chat_url, {'message': 'Test'})
        response = self.client.post(self.chat_url, {'message': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
