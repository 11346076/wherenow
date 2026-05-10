from django.urls import path

from .views import (
    profile,
    edit_profile,
    register,
)

urlpatterns = [

    path(
        'register/',
        register,
        name='register'
    ),

    path(
        'profile/',
        profile,
        name='profile'
    ),

    path(
        'profile/edit/',
        edit_profile,
        name='edit_profile'
    ),
]