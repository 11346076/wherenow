from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class WebPageTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get('/home/')
        self.assertIn(response.status_code, [200, 302])

    def test_explore_page(self):
        response = self.client.get('/explore/')
        self.assertIn(response.status_code, [200, 302])

    def test_admin_page(self):
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [200, 302])


class RestAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_categories_api(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)

    def test_places_api(self):
        response = self.client.get('/api/places/')
        self.assertEqual(response.status_code, 200)

    def test_memories_api(self):
        response = self.client.get('/api/memories/')
        self.assertEqual(response.status_code, 200)

    def test_profiles_api(self):
        response = self.client.get('/api/profiles/')
        self.assertEqual(response.status_code, 200)


class JWTTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_jwt_token_obtain(self):
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class SwaggerTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_swagger_page(self):
        response = self.client.get('/swagger/')
        self.assertEqual(response.status_code, 200)

    def test_redoc_page(self):
        response = self.client.get('/redoc/')
        self.assertEqual(response.status_code, 200)