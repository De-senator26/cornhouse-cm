from django.test import LiveServerTestCase, TestCase, override_settings, Client
from unittest.mock import patch, MagicMock
from google.genai.errors import ClientError
import json
import requests


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
    def test_gemini_quota_error_returns_fallback_reply(self, mock_client_cls):
        # Arrange: make the genai client raise a ClientError with status 429
        mock_client = MagicMock()
        err = ClientError(429, {'error': {'message': 'Quota exceeded'}}, None)
        err.status = 429
        err.status_code = 429
        mock_client.models.generate_content.side_effect = err
        mock_client_cls.return_value = mock_client

        # Act: call the chat API with a (fake) API key present
        with override_settings(GEMINI_API_KEY='fake'):
            resp = self.client.post('/chat/api/', data=json.dumps({'message': 'hello'}), content_type='application/json')

        # Assert: service returns 200 and a friendly keyword fallback message
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue('hello' in data.get('reply', '').lower() or 'farming' in data.get('reply', '').lower())


class ChatbotIntegrationTest(LiveServerTestCase):
    def test_chat_api_returns_fallback_for_quota_error(self):
        with patch('apps.chatbot.views.genai.Client') as mock_client_cls:
            mock_client = MagicMock()
            err = ClientError(429, {'error': {'message': 'Quota exceeded'}}, None)
            err.status = 429
            mock_client.models.generate_content.side_effect = err
            mock_client_cls.return_value = mock_client

            response = requests.post(
                f'{self.live_server_url}/chat/api/',
                json={'message': 'How do I plant maize?'},
                timeout=10,
            )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('plant', data.get('reply', '').lower())
