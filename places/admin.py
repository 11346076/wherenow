from django.contrib import admin
from .models import Category, Tag, Place, PlaceTag, FavoritePlace

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Place)
admin.site.register(PlaceTag)
admin.site.register(FavoritePlace)