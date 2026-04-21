from django.contrib import admin
from .models import CoupleInvitation, CoupleRelationship


@admin.register(CoupleInvitation)
class CoupleInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('sender__username', 'receiver__username')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('邀請資訊', {
            'fields': ('sender', 'receiver', 'status')
        }),
        ('系統資訊', {
            'fields': ('created_at',)
        }),
    )


@admin.register(CoupleRelationship)
class CoupleRelationshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_1', 'user_2', 'is_active', 'anniversary_date', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user_1__username', 'user_2__username')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('關係資訊', {
            'fields': ('user_1', 'user_2', 'is_active', 'anniversary_date')
        }),
        ('系統資訊', {
            'fields': ('created_at',)
        }),
    )
    actions = ['mark_as_active', 'mark_as_inactive']

    @admin.action(description='將選取關係設為啟用')
    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='將選取關係設為停用')
    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)