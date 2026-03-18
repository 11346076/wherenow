from django.contrib import admin
from .models import CoupleInvitation, CoupleRelationship


@admin.register(CoupleInvitation)
class CoupleInvitationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    list_filter = ('status',)


@admin.register(CoupleRelationship)
class CoupleRelationshipAdmin(admin.ModelAdmin):
    list_display = ('user_1', 'user_2', 'is_active', 'created_at')
    list_filter = ('is_active',)