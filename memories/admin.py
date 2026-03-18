from django.contrib import admin
from .models import Memory, MemoryPhoto


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'place', 'visit_date', 'rating', 'cost', 'recommended', 'created_at')
    list_filter = ('recommended', 'visit_date', 'created_at')
    search_fields = ('user__username', 'place__name', 'comment')


@admin.register(MemoryPhoto)
class MemoryPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'memory', 'uploaded_at')
    search_fields = ('memory__comment',)