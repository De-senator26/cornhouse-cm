from django.test import TestCase
from rest_framework.test import APIClient
from apps.users.models import User
from .models import StorageMethod, Harvest, Loss
import datetime


class HarvestModelAndAPITests(TestCase):
    def setUp(self):
        self.farmer = User.objects.create_user(
            username='harvestfarmer',
            password='Password123!',
            phone='+237690000010',
            role='farmer'
        )
        self.storage = StorageMethod.objects.create(
            name='Hermetic Bag',
            description='Airtight bag for grain storage'
        )
        self.harvest = Harvest.objects.create(
            farmer=self.farmer,
            crop_type='maize',
            quantity_kg=500.00,
            harvest_date=datetime.date.today(),
            storage_method=self.storage,
            quality_grade='A'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.farmer)

    def test_storage_method_str(self):
        self.assertEqual(str(self.storage), 'Hermetic Bag')

    def test_harvest_str(self):
        self.assertIn('harvestfarmer', str(self.harvest))
        self.assertIn('500', str(self.harvest))

    def test_loss_creation_and_str(self):
        loss = Loss.objects.create(
            harvest=self.harvest,
            loss_type='spoilage',
            quantity_kg=25.00,
            description='Moisture damage'
        )
        self.assertEqual(str(loss), 'spoilage - 25.0kg')

    def test_harvest_api_list(self):
        response = self.client.get('/api/harvests/harvests/')
        self.assertEqual(response.status_code, 200)
        results = response.json().get('results', response.json())
        self.assertTrue(len(results) >= 1)

    def test_storage_methods_api_list(self):
        response = self.client.get('/api/harvests/storage-methods/')
        self.assertEqual(response.status_code, 200)
