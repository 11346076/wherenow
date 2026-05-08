from rest_framework import serializers, generics

from places.models import (
    Place,
    Category,
    Tag,
    FavoritePlace,
    RandomPickHistory
)

from memories.models import (
    Memory,
    MemoryPhoto
)

from couples.models import (
    CoupleInvitation,
    CoupleRelationship
)

from users.models import Profile


# =========================
# SERIALIZERS
# =========================

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class FavoritePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritePlace
        fields = '__all__'


class RandomPickHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RandomPickHistory
        fields = '__all__'


class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = '__all__'


class MemoryPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryPhoto
        fields = '__all__'


class CoupleInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoupleInvitation
        fields = '__all__'


class CoupleRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoupleRelationship
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


# =========================
# API VIEWS
# =========================

class PlaceListAPI(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class CategoryListAPI(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagListAPI(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FavoritePlaceListAPI(generics.ListCreateAPIView):
    queryset = FavoritePlace.objects.all()
    serializer_class = FavoritePlaceSerializer


class RandomPickHistoryListAPI(generics.ListCreateAPIView):
    queryset = RandomPickHistory.objects.all()
    serializer_class = RandomPickHistorySerializer


class MemoryListAPI(generics.ListCreateAPIView):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer


class MemoryPhotoListAPI(generics.ListCreateAPIView):
    queryset = MemoryPhoto.objects.all()
    serializer_class = MemoryPhotoSerializer


class CoupleInvitationListAPI(generics.ListCreateAPIView):
    queryset = CoupleInvitation.objects.all()
    serializer_class = CoupleInvitationSerializer


class CoupleRelationshipListAPI(generics.ListCreateAPIView):
    queryset = CoupleRelationship.objects.all()
    serializer_class = CoupleRelationshipSerializer


class ProfileListAPI(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer