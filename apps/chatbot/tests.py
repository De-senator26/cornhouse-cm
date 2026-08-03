from django.test import TestCase, override_settings, Client
from unittest.mock import patch, MagicMock
from google.genai.errors import ClientError
import json


class ChatbotAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(GEMINI_API_KEY=None)
    def test_no_api_key_returns_message(self):
        resp = self.client.post('/chat/api/', data=json.dumps({'message': 'hi'}), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('API key not configured', data.get('reply', ''))

    @patch('apps.chatbot.views.genai.Client')
    def test_gemini_quota_error_returns_429(self, mock_client_cls):
        # Arrange: make the genai client raise a ClientError with status 429
        mock_client = MagicMock()
        err = ClientError(429, {'error': {'message': 'Quota exceeded'}}, None)
        # Some ClientError variants expose status or status_code attributes
        err.status = 429
        err.status_code = 429
        mock_client.models.generate_content.side_effect = err
        mock_client_cls.return_value = mock_client

        # Act: call the chat API with a (fake) API key present
        with override_settings(GEMINI_API_KEY='fake'):
            resp = self.client.post('/chat/api/', data=json.dumps({'message': 'hello'}), content_type='application/json')

        # Assert: service returns 429 and a helpful message about quota
        self.assertEqual(resp.status_code, 429)
        data = resp.json()
        self.assertTrue('quota' in data.get('reply', '').lower() or 'exhaust' in data.get('reply', '').lower())
from django.test import TestCase

# Create your tests here.
