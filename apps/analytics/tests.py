from django.test import TestCase, Client
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User
from apps.harvests.models import Harvest


class AnalyticsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.partner = User.objects.create_user(
            username='partneruser',
            email='partner@example.com',
            password='Password123!',
            role='partner'
        )
        self.farmer = User.objects.create_user(
            username='farmeruser',
            email='farmer2@example.com',
            password='Password123!',
            role='farmer'
        )
        Harvest.objects.create(
            farmer=self.farmer,
            quantity_kg=100.5,
            harvest_date='2026-08-01',
            quality_grade='A'
        )
        refresh = RefreshToken.for_user(self.partner)
        self.partner_token = str(refresh.access_token)

    def test_dashboard_stats_as_partner(self):
        response = self.client.get(
            '/api/analytics/stats/',
            HTTP_AUTHORIZATION=f'Bearer {self.partner_token}'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total_farmers', data)
        self.assertIn('total_harvests', data)
        self.assertIn('harvests_by_month', data)
        self.assertEqual(data['total_farmers'], 1)
        self.assertEqual(data['total_harvests'], 1)

    def test_dashboard_stats_forbidden_for_farmer(self):
        farmer_refresh = RefreshToken.for_user(self.farmer)
        farmer_token = str(farmer_refresh.access_token)
        response = self.client.get(
            '/api/analytics/stats/',
            HTTP_AUTHORIZATION=f'Bearer {farmer_token}'
        )
        self.assertEqual(response.status_code, 403)
