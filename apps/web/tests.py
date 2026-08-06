from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User
from apps.web.models import UserFeedback


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

    def test_submit_feedback_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post('/feedback/', {
            'rating': '5',
            'category': 'post_harvest',
            'role': 'farmer',
            'comment': 'CornHouse hermetic bag tips saved 30% of my harvest!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserFeedback.objects.filter(user=self.user).exists())
        feedback = UserFeedback.objects.get(user=self.user)
        self.assertEqual(feedback.rating, 5)
        self.assertEqual(feedback.category, 'post_harvest')

    def test_submit_feedback_anonymous(self):
        response = self.client.post('/feedback/', {
            'name': 'Emmanuel N.',
            'rating': '4',
            'category': 'marketplace',
            'role': 'buyer',
            'comment': 'Great marketplace for sourcing quality maize in bulk.'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserFeedback.objects.filter(name='Emmanuel N.').exists())

    def test_submit_feedback_empty_comment_fails(self):
        response = self.client.post('/feedback/', {
            'rating': '5',
            'comment': ''
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter your feedback comments')
        self.assertEqual(UserFeedback.objects.count(), 0)

    def test_home_page_displays_public_reviews(self):
        UserFeedback.objects.create(
            name='Amina B.',
            rating=5,
            category='chatbot',
            role='farmer',
            comment='The AI Agribot gave instant advice on pest management.',
            is_public=True
        )
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Amina B.')
        self.assertContains(response, 'AI Agribot gave instant advice')
