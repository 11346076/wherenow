from django.urls import path
from .views import profile, edit_profile

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]