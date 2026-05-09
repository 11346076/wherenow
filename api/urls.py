from django.urls import path

from .views import (
    PlaceListAPI,
    PlaceDetailAPI,

    CategoryListAPI,
    CategoryDetailAPI,

    TagListAPI,
    TagDetailAPI,

    FavoritePlaceListAPI,
    FavoritePlaceDetailAPI,

    RandomPickHistoryListAPI,
    RandomPickHistoryDetailAPI,

    MemoryListAPI,
    MemoryDetailAPI,

    MemoryPhotoListAPI,
    MemoryPhotoDetailAPI,

    CoupleInvitationListAPI,
    CoupleInvitationDetailAPI,

    CoupleRelationshipListAPI,
    CoupleRelationshipDetailAPI,

    ProfileListAPI,
    ProfileDetailAPI,
)

urlpatterns = [

    # Places
    path('places/', PlaceListAPI.as_view()),
    path('places/<int:pk>/', PlaceDetailAPI.as_view()),

    # Categories
    path('categories/', CategoryListAPI.as_view()),
    path('categories/<int:pk>/', CategoryDetailAPI.as_view()),

    # Tags
    path('tags/', TagListAPI.as_view()),
    path('tags/<int:pk>/', TagDetailAPI.as_view()),

    # Favorites
    path('favorites/', FavoritePlaceListAPI.as_view()),
    path('favorites/<int:pk>/', FavoritePlaceDetailAPI.as_view()),

    # Random Pick Histories
    path('random-picks/', RandomPickHistoryListAPI.as_view()),
    path('random-picks/<int:pk>/', RandomPickHistoryDetailAPI.as_view()),

    # Memories
    path('memories/', MemoryListAPI.as_view()),
    path('memories/<int:pk>/', MemoryDetailAPI.as_view()),

    # Memory Photos
    path('memory-photos/', MemoryPhotoListAPI.as_view()),
    path('memory-photos/<int:pk>/', MemoryPhotoDetailAPI.as_view()),

    # Couple Invitations
    path('couple-invitations/', CoupleInvitationListAPI.as_view()),
    path('couple-invitations/<int:pk>/', CoupleInvitationDetailAPI.as_view()),

    # Couple Relationships
    path('couple-relationships/', CoupleRelationshipListAPI.as_view()),
    path('couple-relationships/<int:pk>/', CoupleRelationshipDetailAPI.as_view()),

    # Profiles
    path('profiles/', ProfileListAPI.as_view()),
    path('profiles/<int:pk>/', ProfileDetailAPI.as_view()),
]