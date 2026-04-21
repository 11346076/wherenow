from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('shared/', views.shared_place_list, name='shared_place_list'),

    path('create/', views.place_create, name='place_create'),
    path('<int:pk>/', views.place_detail, name='place_detail'),
    path('<int:pk>/edit/', views.place_update, name='place_update'),
    path('<int:pk>/delete/', views.place_delete, name='place_delete'),

    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorite/add/<int:place_id>/', views.add_favorite, name='add_favorite'),
    path('favorite/remove/<int:place_id>/', views.remove_favorite, name='remove_favorite'),

    path('random-pick/', views.random_pick, name='random_pick'),
    path('random-pick-history/', views.random_pick_history, name='random_pick_history'),
]