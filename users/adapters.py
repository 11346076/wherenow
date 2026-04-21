from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from .models import Profile


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        extra_data = sociallogin.account.extra_data

        email = (data.get("email") or extra_data.get("email") or "").strip()
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

        extra_data = sociallogin.account.extra_data
        profile, created = Profile.objects.get_or_create(user=user)

        # 如果 nickname 還沒填，就先用 Google 名字或 username
        if not profile.nickname:
            google_name = (
                extra_data.get("name")
                or f"{user.first_name} {user.last_name}".strip()
                or user.username
            )
            profile.nickname = google_name

        # 抓 Google 頭貼，只在目前沒有 avatar 時才抓
        avatar_url = extra_data.get("picture")
        if avatar_url and not profile.avatar:
            try:
                response = urlopen(avatar_url)
                image_data = response.read()
                file_name = f"{user.username}_google.jpg"
                profile.avatar.save(file_name, ContentFile(image_data), save=False)
            except (URLError, HTTPError, Exception):
                pass

        profile.save()
        return user