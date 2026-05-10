from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users.views import custom_login_view

from .views import (
    root_redirect,
    home,
    explore_page,
    dashboard,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="WhereNow API",
        default_version='v1',
        description="WhereNow 地點清單與情侶回憶管理系統 API 文件",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # CAPTCHA
    path('captcha/', include('captcha.urls')),

    # 客製化登入頁
    path('accounts/login/', custom_login_view, name='account_login'),

    # allauth
    path('accounts/', include('allauth.urls')),

    # i18n
    path('i18n/', include('django.conf.urls.i18n')),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API
    path('api/', include('api.urls')),

    # select2
    path('select2/', include('django_select2.urls')),

    # 首頁
    path('', root_redirect, name='root'),

    path('home/', home, name='home'),

    path('explore/', explore_page, name='explore_page'),

    path('dashboard/', dashboard, name='dashboard'),

    path('users/', include('users.urls')),

    path('couples/', include('couples.urls')),

    path('places/', include('places.urls')),

    path('memories/', include('memories.urls')),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)