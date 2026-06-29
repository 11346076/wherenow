import logging

from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from .models import Profile

logger = logging.getLogger('wherenow')


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def _get_social_email(self, sociallogin, data=None):
        extra_data = sociallogin.account.extra_data or {}
        data = data or {}
        return (
            data.get("email")
            or extra_data.get("email")
            or getattr(sociallogin.user, "email", "")
            or ""
        ).strip().lower()

    def _sync_user_and_profile(self, user, sociallogin):
        extra_data = sociallogin.account.extra_data or {}
        email = self._get_social_email(sociallogin)
        first_name = (extra_data.get("given_name") or "").strip()
        last_name = (extra_data.get("family_name") or "").strip()
        google_name = (
            extra_data.get("name")
            or f"{first_name} {last_name}".strip()
            or user.username
        )

        changed = False
        if email and not user.email:
            user.email = email
            changed = True
        if first_name and not user.first_name:
            user.first_name = first_name
            changed = True
        if last_name and not user.last_name:
            user.last_name = last_name
            changed = True
        if changed:
            user.save(update_fields=['email', 'first_name', 'last_name'])

        if email:
            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=email,
                defaults={
                    'primary': not EmailAddress.objects.filter(user=user).exists(),
                    'verified': True,
                },
            )
            if not email_address.verified:
                email_address.verified = True
                email_address.save(update_fields=['verified'])

        profile, created = Profile.objects.get_or_create(user=user)
        if not profile.nickname:
            profile.nickname = google_name

        avatar_url = extra_data.get("picture")
        if avatar_url and not profile.avatar:
            try:
                response = urlopen(avatar_url, timeout=8)
                image_data = response.read()
                file_name = f"{user.username}_google.jpg"
                profile.avatar.save(file_name, ContentFile(image_data), save=False)
            except (URLError, HTTPError, Exception) as exc:
                logger.info("Google avatar sync skipped: %s", exc)

        profile.save()

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            self._sync_user_and_profile(sociallogin.user, sociallogin)
            return

        email = self._get_social_email(sociallogin)
        if not email:
            return

        existing_user = (
            User.objects.filter(email__iexact=email)
            .order_by('id')
            .first()
        )

        if existing_user is None:
            return

        sociallogin.connect(request, existing_user)
        self._sync_user_and_profile(existing_user, sociallogin)
        logger.info(
            "Linked Google login to existing user by email: user_id=%s email=%s",
            existing_user.pk,
            email,
        )

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        extra_data = sociallogin.account.extra_data

        email = self._get_social_email(sociallogin, data)
        first_name = (data.get("first_name") or extra_data.get("given_name") or "").strip()
        last_name = (data.get("last_name") or extra_data.get("family_name") or "").strip()
        full_name = (data.get("name") or extra_data.get("name") or "").strip()

        if email:
            user.email = email

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        # 產生不重複的 username
        if email:
            base_username = email.split("@")[0].strip()
        elif full_name:
            base_username = full_name.replace(" ", "").strip()
        elif first_name or last_name:
            base_username = f"{first_name}{last_name}".replace(" ", "").strip()
        else:
            base_username = "googleuser"

        if not base_username:
            base_username = "googleuser"

        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user.username = username
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        self._sync_user_and_profile(user, sociallogin)
        return user
