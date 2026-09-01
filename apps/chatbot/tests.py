"""Tests for the CornHouse chatbot — fallback logic and API endpoint."""
from django.test import TestCase, Client, override_settings
from unittest.mock import patch, MagicMock
from google.genai.errors import ClientError
from apps.chatbot.fallback import get_fallback_reply
import json


# ─────────────────────────────────────────────────────────────────────────────
# 1. Unit tests for the fallback knowledge base
# ─────────────────────────────────────────────────────────────────────────────

class FallbackKnowledgeBaseTest(TestCase):
    """Verify every topic branch returns useful content and never the old
    'I don't have the AI backend' message."""

    BANNED_PHRASES = [
        "i don't have the ai backend",
        "right now",
        "backend",
    ]

    def _assert_clean(self, reply: str, topic: str):
        lower = reply.lower()
        for phrase in self.BANNED_PHRASES:
            self.assertNotIn(
                phrase, lower,
                msg=f"Topic '{topic}': banned phrase '{phrase}' found in reply."
            )
        self.assertGreater(len(reply), 30, msg=f"Topic '{topic}': reply is too short.")

    def test_empty_message_returns_welcome(self):
        reply = get_fallback_reply("")
        self._assert_clean(reply, "empty")
        self.assertIn("assistant", reply.lower())

    def test_none_message_returns_welcome(self):
        reply = get_fallback_reply(None)
        self._assert_clean(reply, "none")

    def test_greeting_hi(self):
        reply = get_fallback_reply("hi")
        self._assert_clean(reply, "greeting-hi")
        self.assertIn("hello", reply.lower())

    def test_greeting_bonjour(self):
        reply = get_fallback_reply("bonjour")
        self._assert_clean(reply, "greeting-bonjour")

    def test_planting_question(self):
        reply = get_fallback_reply("How do I plant maize seeds?")
        self._assert_clean(reply, "planting")
        self.assertIn("plant", reply.lower())

    def test_sowing_keyword(self):
        reply = get_fallback_reply("When should I sow?")
        self._assert_clean(reply, "sowing")

    def test_fall_armyworm(self):
        reply = get_fallback_reply("I have fall armyworm attacking my crop")
        self._assert_clean(reply, "fall armyworm")
        self.assertIn("armyworm", reply.lower())

    def test_pest_keyword(self):
        reply = get_fallback_reply("What pests should I watch for?")
        self._assert_clean(reply, "pest")

    def test_disease_keyword(self):
        reply = get_fallback_reply("My maize has a disease — leaves are spotted")
        self._assert_clean(reply, "disease")

    def test_fertilizer_npk(self):
        reply = get_fallback_reply("Which NPK fertilizer should I apply?")
        self._assert_clean(reply, "fertilizer-npk")
        self.assertIn("npk", reply.lower())

    def test_urea_top_dressing(self):
        reply = get_fallback_reply("When do I top dress with urea?")
        self._assert_clean(reply, "urea")

    def test_water_irrigation(self):
        reply = get_fallback_reply("How much water does maize need?")
        self._assert_clean(reply, "irrigation")

    def test_drought_stress(self):
        reply = get_fallback_reply("My field is suffering from drought")
        self._assert_clean(reply, "drought")

    def test_harvest_timing(self):
        reply = get_fallback_reply("When is the right time to harvest?")
        self._assert_clean(reply, "harvest")
        self.assertIn("harvest", reply.lower())

    def test_grain_drying(self):
        reply = get_fallback_reply("How do I dry my grain after harvest?")
        self._assert_clean(reply, "drying")

    def test_storage_aflatoxin(self):
        reply = get_fallback_reply("How do I store grain without aflatoxin?")
        self._assert_clean(reply, "storage-aflatoxin")
        self.assertIn("aflatoxin", reply.lower())

    def test_market_price(self):
        reply = get_fallback_reply("What is the market price for maize?")
        self._assert_clean(reply, "market")
        self.assertIn("price", reply.lower())

    def test_sell_keyword(self):
        reply = get_fallback_reply("Where can I sell my maize?")
        self._assert_clean(reply, "sell")

    def test_soil_preparation(self):
        reply = get_fallback_reply("How do I prepare my soil for planting?")
        self._assert_clean(reply, "soil")

    def test_weed_control(self):
        reply = get_fallback_reply("What herbicide should I use for weeds?")
        self._assert_clean(reply, "weed")

    def test_variety_selection(self):
        reply = get_fallback_reply("Which maize variety should I plant?")
        self._assert_clean(reply, "variety")

    def test_hybrid_keyword(self):
        reply = get_fallback_reply("Are hybrid seeds better than OPV?")
        self._assert_clean(reply, "hybrid")

    def test_grant_finance(self):
        reply = get_fallback_reply("Can I get a grant for my farm?")
        self._assert_clean(reply, "grant")

    def test_loan_keyword(self):
        reply = get_fallback_reply("Where can I get a loan for farming?")
        self._assert_clean(reply, "loan")

    def test_unknown_topic_default(self):
        """Unknown topics must never return the old backend message."""
        reply = get_fallback_reply("What is the capital of France?")
        self._assert_clean(reply, "unknown")
        # Should still give a helpful menu
        self.assertIn("maize", reply.lower())

    def test_completely_random_input(self):
        reply = get_fallback_reply("xyzzy frobnicator 12345")
        self._assert_clean(reply, "random")


# ─────────────────────────────────────────────────────────────────────────────
# 2. API endpoint tests
# ─────────────────────────────────────────────────────────────────────────────

class ChatAPIEndpointTest(TestCase):
    """Test the /chat/api/ view returns correct status codes and clean replies."""

    def setUp(self):
        self.client = Client()

    def _post(self, message):
        return self.client.post(
            '/chat/api/',
            data=json.dumps({'message': message}),
            content_type='application/json',
        )

    @override_settings(GEMINI_API_KEY=None)
    def test_no_api_key_returns_200(self):
        resp = self._post("hi")
        self.assertEqual(resp.status_code, 200)

    @override_settings(GEMINI_API_KEY=None)
    def test_no_api_key_reply_has_no_backend_message(self):
        resp = self._post("hello")
        data = resp.json()
        reply = data.get('reply', '').lower()
        self.assertNotIn("backend", reply)
        self.assertNotIn("right now", reply)

    @override_settings(GEMINI_API_KEY=None)
    def test_planting_question_via_api(self):
        resp = self._post("How do I plant maize?")
        data = resp.json()
        self.assertIn("plant", data.get('reply', '').lower())

    @override_settings(GEMINI_API_KEY=None)
    def test_pest_question_via_api(self):
        resp = self._post("I have armyworm on my farm")
        data = resp.json()
        self.assertIn("armyworm", data.get('reply', '').lower())

    @override_settings(GEMINI_API_KEY=None)
    def test_fertilizer_question_via_api(self):
        resp = self._post("What NPK fertilizer should I use?")
        data = resp.json()
        self.assertIn("npk", data.get('reply', '').lower())

    @override_settings(GEMINI_API_KEY=None)
    def test_empty_message_returns_400(self):
        resp = self._post("")
        self.assertEqual(resp.status_code, 400)

    def test_get_method_returns_405(self):
        resp = self.client.get('/chat/api/')
        self.assertEqual(resp.status_code, 405)

    @patch('apps.chatbot.views.genai.Client')
    def test_gemini_quota_error_returns_fallback(self, mock_client_cls):
        """When Gemini returns a 429 quota error, fallback kicks in cleanly."""
        mock_client = MagicMock()
        err = ClientError(429, {'error': {'message': 'Quota exceeded'}}, None)
        err.status = 429
        err.status_code = 429
        mock_client.models.generate_content.side_effect = err
        mock_client_cls.return_value = mock_client

        with override_settings(GEMINI_API_KEY='fake-key'):
            resp = self._post("hello")

        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        reply = data.get('reply', '').lower()
        self.assertNotIn("backend", reply)
        self.assertTrue(len(reply) > 10)

    @patch('apps.chatbot.views.genai.Client')
    def test_gemini_general_error_returns_fallback(self, mock_client_cls):
        """Any unexpected Gemini error also falls back gracefully."""
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("Connection timeout")
        mock_client_cls.return_value = mock_client

        with override_settings(GEMINI_API_KEY='fake-key'):
            resp = self._post("what fertilizer should I use?")

        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("npk", data.get('reply', '').lower())
