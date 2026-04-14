from django.db import models
from django.contrib.auth.models import User


# -----------------------------
# Category（地點分類）
# -----------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


# -----------------------------
# Tag（標籤）
# -----------------------------
class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# -----------------------------
# Place（地點）
# -----------------------------
class Place(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='places'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='places'
    )

    name = models.CharField(max_length=255)
    area = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)

    google_map_link = models.URLField(blank=True)
    note = models.TextField(blank=True)

    budget = models.IntegerField(default=0)

    is_public = models.BooleanField(default=False)
    is_visited = models.BooleanField(default=False)
    shared_with_couple = models.BooleanField(default=False)

    tags = models.ManyToManyField(
        Tag,
        through='PlaceTag',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # 最新的在最上面

    def __str__(self):
        return f"{self.name} ({self.user.username})"


# -----------------------------
# PlaceTag（地點-標籤關聯）
# -----------------------------
class PlaceTag(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('place', 'tag')  # 防止重複標籤

    def __str__(self):
        return f"{self.place.name} - {self.tag.name}"


# -----------------------------
# FavoritePlace（收藏地點）
# -----------------------------
class FavoritePlace(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_places'
    )

    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place')  # 防止重複收藏
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.place.name}"


# -----------------------------
# RandomPickHistory（抽選紀錄）
# -----------------------------
class RandomPickHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='random_pick_histories'
    )

    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='random_pick_histories'
    )

    picked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-picked_at']

    def __str__(self):
        return f"{self.user.username} 抽到了 {self.place.name}"