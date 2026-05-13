def get_partner(user):
    from .models import CoupleRelationship
    relationship = CoupleRelationship.objects.filter(
        user_1=user,
        is_active=True
    ).first()
    if relationship:
        return relationship.user_2
    relationship = CoupleRelationship.objects.filter(
        user_2=user,
        is_active=True
    ).first()
    if relationship:
        return relationship.user_1
    return None
