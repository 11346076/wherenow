from django.urls import path

from .views import (
    PlaceListAPI,
    CategoryListAPI,
    TagListAPI,
    FavoritePlaceListAPI,
    RandomPickHistoryListAPI,
    MemoryListAPI,
    MemoryPhotoListAPI,
    CoupleInvitationListAPI,
    CoupleRelationshipListAPI,
    ProfileListAPI,
)

urlpatterns = [

    # Places
    path('places/', PlaceListAPI.as_view()),

    # Categories
    path('categories/', CategoryListAPI.as_view()),

    # Tags
    path('tags/', TagListAPI.as_view()),

    # Favorites
    path('favorites/', FavoritePlaceListAPI.as_view()),

    # Random Pick Histories
    path('random-picks/', RandomPickHistoryListAPI.as_view()),

    # Memories
    path('memories/', MemoryListAPI.as_view()),

    # Memory Photos
    path('memory-photos/', MemoryPhotoListAPI.as_view()),

    # Couple Invitations
    path('couple-invitations/', CoupleInvitationListAPI.as_view()),

    # Couple Relationships
    path('couple-relationships/', CoupleRelationshipListAPI.as_view()),

    # Profiles
    path('profiles/', ProfileListAPI.as_view()),
]