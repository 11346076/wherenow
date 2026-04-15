from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        extra_data = sociallogin.account.extra_data

        email = (
            data.get("email")
            or extra_data.get("email")
            or ""
        ).strip()

        first_name = (
            data.get("first_name")
            or extra_data.get("given_name")
            or ""
        ).strip()

        last_name = (
            data.get("last_name")
            or extra_data.get("family_name")
            or ""
        ).strip()

        full_name = (
            data.get("name")
            or extra_data.get("name")
            or ""
        ).strip()

        if email:
            user.email = email

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        # 一定要產生一個不為空、且不重複的 username
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