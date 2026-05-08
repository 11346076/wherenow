from django.db import models
from django.contrib.auth.models import User


# -----------------------------
# Category（地點分類）
# -----------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


# -----------------------------
# Tag（標籤）
# -----------------------------
class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


# -----------------------------
# Place（地點）
# -----------------------------
class Place(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='places',
        db_index=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='places',
        db_index=True
    )

    name = models.CharField(max_length=255, db_index=True)
    area = models.CharField(max_length=100, db_index=True)
    address = models.CharField(max_length=255, blank=True)

    google_map_link = models.URLField(blank=True)
    note = models.TextField(blank=True)

    budget = models.IntegerField(default=0)

    image = models.ImageField(upload_to='places/', blank=True, null=True)

    is_public = models.BooleanField(default=False, db_index=True)
    is_visited = models.BooleanField(default=False, db_index=True)
    shared_with_couple = models.BooleanField(default=False, db_index=True)

    tags = models.ManyToManyField(
        Tag,
        through='PlaceTag',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['category']),
            models.Index(fields=['name']),
            models.Index(fields=['area']),
            models.Index(fields=['is_public']),
            models.Index(fields=['shared_with_couple']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['user', 'is_public']),
        ]

    def __str__(self):
        return f"{self.name} ({self.user.username})"


# -----------------------------
# PlaceTag（地點-標籤關聯）
# -----------------------------
class PlaceTag(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        db_index=True
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        unique_together = ('place', 'tag')
        indexes = [
            models.Index(fields=['place']),
            models.Index(fields=['tag']),
            models.Index(fields=['place', 'tag']),
        ]

    def __str__(self):
        return f"{self.place.name} - {self.tag.name}"


# -----------------------------
# FavoritePlace（收藏地點）
# -----------------------------
class FavoritePlace(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_places',
        db_index=True
    )

    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('user', 'place')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['place']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.place.name}"


# -----------------------------
# RandomPickHistory（抽選紀錄）
# -----------------------------
class RandomPickHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='random_pick_histories',
        db_index=True
    )

    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='random_pick_histories',
        db_index=True
    )

    picked_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-picked_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['place']),
            models.Index(fields=['picked_at']),
            models.Index(fields=['user', 'picked_at']),
        ]

    def __str__(self):
        return f"{self.user.username} 抽到了 {self.place.name}"