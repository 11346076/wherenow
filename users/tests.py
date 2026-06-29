from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase

from users.adapters import CustomSocialAccountAdapter
from users.forms import RegisterForm


class _FakeAccount:
    def __init__(self, extra_data):
        self.extra_data = extra_data


class _FakeSocialLogin:
    is_existing = False

    def __init__(self, email):
        self.account = _FakeAccount({
            'email': email,
            'name': 'Google User',
            'given_name': 'Google',
            'family_name': 'User',
        })
        self.user = User(email=email, username='googleuser')
        self.connected_user = None

    def connect(self, request, user):
        self.connected_user = user


class RegisterFormTests(TestCase):
    def test_email_must_be_unique_case_insensitive(self):
        User.objects.create_user(
            username='email-user',
            email='SameEmail@example.com',
            password='password123',
        )

        form = RegisterForm()
        form.cleaned_data = {'email': 'sameemail@example.com'}

        with self.assertRaises(ValidationError):
            form.clean_email()


class GoogleEmailBindingTests(TestCase):
    def test_google_login_reuses_existing_user_by_email(self):
        existing_user = User.objects.create_user(
            username='local-user',
            email='bind@example.com',
            password='password123',
        )
        existing_profile = existing_user.profile
        request = RequestFactory().get('/accounts/google/login/callback/')
        sociallogin = _FakeSocialLogin('BIND@example.com')

        CustomSocialAccountAdapter().pre_social_login(request, sociallogin)

        self.assertEqual(sociallogin.connected_user, existing_user)
        existing_user.refresh_from_db()
        self.assertEqual(existing_user.profile.pk, existing_profile.pk)
        self.assertEqual(
            User.objects.filter(email__iexact='bind@example.com').count(),
            1,
        )
