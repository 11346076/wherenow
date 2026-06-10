from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from .models import Category


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


class PlaceFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='placeformuser',
            password='testpass123'
        )
        Category.objects.create(name='餐廳')

    def test_place_create_renders_category_options(self):
        self.client.force_login(self.user)

        response = self.client.get('/places/create/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<option value="', html=False)
        self.assertContains(response, '餐廳')
