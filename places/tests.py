from django.test import TestCase
from rest_framework.test import APIClient


class HomePageTest(TestCase):

    def test_home_page_redirect_or_success(self):
        response = self.client.get('/home/')
        self.assertIn(response.status_code, [200, 302])


class APITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_api_categories(self):
        response = self.client.get('/api/categories/')
        self.assertIn(response.status_code, [200, 301, 302])