from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('create/', views.place_create, name='place_create'),
    path('<int:pk>/', views.place_detail, name='place_detail'),
    path('<int:pk>/edit/', views.place_update, name='place_update'),
    path('<int:pk>/delete/', views.place_delete, name='place_delete'),
]