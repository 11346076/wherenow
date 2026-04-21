from django.contrib import admin
from .models import Category, Tag, Place, PlaceTag, FavoritePlace, RandomPickHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


class PlaceTagInline(admin.TabularInline):
    model = PlaceTag
    extra = 1


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'user',
        'category',
        'area',
        'budget',
        'is_public',
        'is_visited',
        'shared_with_couple',
        'created_at',
    )
    list_filter = (
        'category',
        'is_public',
        'is_visited',
        'shared_with_couple',
        'created_at',
    )
    search_fields = (
        'name',
        'area',
        'address',
        'user__username',
        'note',
    )
    readonly_fields = ('created_at',)
    fieldsets = (
        ('基本資訊', {
            'fields': ('user', 'category', 'name', 'area', 'address')
        }),
        ('詳細內容', {
            'fields': ('google_map_link', 'note', 'budget')
        }),
        ('狀態設定', {
            'fields': ('is_public', 'is_visited', 'shared_with_couple')
        }),
        ('系統資訊', {
            'fields': ('created_at',)
        }),
    )
    inlines = [PlaceTagInline]
    actions = ['mark_as_public', 'mark_as_private', 'mark_as_visited']

    @admin.action(description='將選取地點設為公開')
    def mark_as_public(self, request, queryset):
        queryset.update(is_public=True)

    @admin.action(description='將選取地點設為不公開')
    def mark_as_private(self, request, queryset):
        queryset.update(is_public=False)

    @admin.action(description='將選取地點設為已拜訪')
    def mark_as_visited(self, request, queryset):
        queryset.update(is_visited=True)


@admin.register(PlaceTag)
class PlaceTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'tag')
    list_filter = ('tag',)
    search_fields = ('place__name', 'tag__name')


@admin.register(FavoritePlace)
class FavoritePlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'place', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'place__name')
    readonly_fields = ('created_at',)


@admin.register(RandomPickHistory)
class RandomPickHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'place', 'picked_at')
    list_filter = ('picked_at',)
    search_fields = ('user__username', 'place__name')
    readonly_fields = ('picked_at',)