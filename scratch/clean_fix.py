import os
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

# Step 1: Clean all existing SocialApps
deleted = SocialApp.objects.all().delete()
print(f"Deleted: {deleted}")

# Step 2: Ensure Site 1 is correct
s1, _ = Site.objects.update_or_create(
    id=1,
    defaults={'domain': '127.0.0.1:8000', 'name': 'Localhost Dev'}
)
print(f"Site 1: {s1.domain}")

# Step 3: Create a fresh SocialApp with correct credentials
client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')
print(f"Client ID from env: {client_id[:30]}...")
print(f"Secret from env: {secret[:10]}...")

app = SocialApp.objects.create(
    provider='google',
    name='Google',
    client_id=client_id,
    secret=secret,
    key='',
)

# Step 4: Link to Site 1
app.sites.add(s1)

print(f"Created SocialApp ID={app.id}")
print(f"Linked to: {list(app.sites.all())}")
print("Done!")
