from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User


class WebFrontendTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testfarmer',
            email='farmer@example.com',
            password='Password123!',
            phone='+237690000001',
            role='farmer'
        )

    def test_home_page_renders(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Empowering')

    def test_successful_registration(self):
        response = self.client.post('/register/', {
            'username': 'newfarmer',
            'email': 'new@example.com',
            'phone': '+237690000002',
            'role': 'farmer',
            'password': 'Password123!',
            'password_confirm': 'Password123!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newfarmer').exists())

    def test_registration_password_mismatch(self):
        response = self.client.post('/register/', {
            'username': 'badfarmer',
            'email': 'bad@example.com',
            'phone': '+237690000003',
            'role': 'farmer',
            'password': 'Password123!',
            'password_confirm': 'Different123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match')

    def test_successful_login(self):
        response = self.client.post('/login/', {
            'username': 'testfarmer',
            'password': 'Password123!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', self.client.session)
        self.assertIn('refresh_token', self.client.session)
        self.assertEqual(self.client.session['user'], 'testfarmer')

    def test_login_incorrect_password(self):
        response = self.client.post('/login/', {
            'username': 'testfarmer',
            'password': 'WrongPassword!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Incorrect password')

    def test_login_nonexistent_user(self):
        response = self.client.post('/login/', {
            'username': 'unknownuser',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No account found')
