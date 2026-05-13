from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

# Fix Site 1
try:
    s1 = Site.objects.get(id=1)
    s1.domain = '127.0.0.1:8000'
    s1.name = 'Localhost (127.0.0.1)'
    s1.save()
    print('Site 1 updated successfully to 127.0.0.1:8000')
except Site.DoesNotExist:
    print('Site 1 not found!')

# Link SocialApp
apps = SocialApp.objects.all()
if apps.exists():
    for app in apps:
        app.sites.add(s1)
        print(f'SocialApp "{app.name}" linked to Site 1')
else:
    print('No SocialApp found in database.')
