from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import root_redirect, home

urlpatterns = [
    path('admin/', admin.site.urls),

    # allauth
    path('accounts/', include('allauth.urls')),

    # 首頁先判斷登入狀態
    path('', root_redirect, name='root'),

    # 真正首頁
    path('home/', home, name='home'),

    path('users/', include('users.urls')),
    path('couples/', include('couples.urls')),
    path('places/', include('places.urls')),
    path('memories/', include('memories.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    