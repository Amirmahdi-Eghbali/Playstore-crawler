from django.test import TestCase
import psycopg2
from rest_framework.test import APIClient
from rest_framework import status

class AppNameViewSetTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.app_data = {
            'app_id': 'com.whatsapp',
            'genre': 'messenger'
        }

    def test_create_app(self):
        response = self.client.post('/app-names/', self.app_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['app_id'], self.app_data['app_id'])

    def test_get_app_list(self):
        self.client.post('/app-names/', self.app_data, format='json')
        response = self.client.get('/app-names/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)