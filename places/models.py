from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Place(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='places')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='places')

    name = models.CharField(max_length=255)
    area = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    google_map_link = models.URLField(blank=True)
    note = models.TextField(blank=True)
    budget = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    is_visited = models.BooleanField(default=False)
    shared_with_couple = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, through='PlaceTag', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PlaceTag(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.place.name} - {self.tag.name}"


class FavoritePlace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_places')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place')

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.place.name}"


class RandomPickHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='random_pick_histories')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='random_pick_histories')
    picked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} 抽到了 {self.place.name}"