from django import template
from couples.models import CoupleInvitation

register = template.Library()


@register.simple_tag
def pending_invitation_count(user):
    if not user.is_authenticated:
        return 0

    return CoupleInvitation.objects.filter(
        receiver=user,
        status='pending'
    ).count()