from django.contrib import admin
from .models import Memory, MemoryPhoto


class MemoryPhotoInline(admin.TabularInline):
    model = MemoryPhoto
    extra = 1


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'place',
        'visit_date',
        'rating',
        'cost',
        'recommended',
        'shared_with_couple',
        'is_public',
        'created_at',
    )
    list_filter = (
        'recommended',
        'shared_with_couple',
        'is_public',
        'visit_date',
        'created_at',
    )
    search_fields = (
        'user__username',
        'place__name',
        'comment',
    )
    readonly_fields = ('created_at',)
    fieldsets = (
        ('基本資訊', {
            'fields': ('user', 'place', 'visit_date')
        }),
        ('內容與評價', {
            'fields': ('comment', 'rating', 'cost', 'recommended')
        }),
        ('分享設定', {
            'fields': ('shared_with_couple', 'is_public')
        }),
        ('系統資訊', {
            'fields': ('created_at',)
        }),
    )
    inlines = [MemoryPhotoInline]
    actions = ['mark_as_public', 'mark_as_private', 'mark_as_recommended']

    @admin.action(description='將選取回憶設為公開')
    def mark_as_public(self, request, queryset):
        queryset.update(is_public=True)

    @admin.action(description='將選取回憶設為不公開')
    def mark_as_private(self, request, queryset):
        queryset.update(is_public=False)

    @admin.action(description='將選取回憶設為推薦')
    def mark_as_recommended(self, request, queryset):
        queryset.update(recommended=True)


@admin.register(MemoryPhoto)
class MemoryPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'memory', 'uploaded_at')
    search_fields = ('memory__comment', 'memory__place__name', 'memory__user__username')
    readonly_fields = ('uploaded_at',)