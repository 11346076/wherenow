from django.urls import path
from . import views

urlpatterns = [
    path('', views.memory_list, name='memory_list'),
    path('shared/', views.shared_memory_list, name='shared_memory_list'),
    path('create/', views.memory_create, name='memory_create'),
    path('<int:pk>/', views.memory_detail, name='memory_detail'),
    path('<int:pk>/edit/', views.memory_edit, name='memory_edit'),
    path('<int:pk>/delete/', views.memory_delete, name='memory_delete'),
    path('photo/<int:pk>/delete/', views.memory_photo_delete, name='memory_photo_delete'),
    path('public-search/', views.public_memory_search, name='public_memory_search'),
]