from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings

print(f'SITE_ID in settings: {settings.SITE_ID}')

try:
    s = Site.objects.get(id=settings.SITE_ID)
    print(f'Site with SITE_ID: ID={s.id}, Domain={s.domain}')
except Site.DoesNotExist:
    print(f'CRITICAL: Site with ID {settings.SITE_ID} does not exist!')

all_sites = Site.objects.all()
print('All Sites in DB:')
for site in all_sites:
    print(f'  ID={site.id}, Domain={site.domain}, Name={site.name}')

all_apps = SocialApp.objects.all()
print(f'All SocialApps in DB: {len(all_apps)}')
for app in all_apps:
    print(f'  ID={app.id}, Provider={app.provider}, Name={app.name}')
    print(f'  Linked Sites: {[site.id for site in app.sites.all()]}')

# Try to find app for current site
current_site_apps = SocialApp.objects.filter(sites__id=settings.SITE_ID, provider='google')
print(f'Google apps for current site (ID {settings.SITE_ID}): {list(current_site_apps)}')
