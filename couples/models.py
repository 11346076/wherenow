from django.db import models
from django.contrib.auth.models import User


class CoupleInvitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_invitations'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_invitations'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"


class CoupleRelationship(models.Model):
    user_1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relationship_user1'
    )
    user_2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relationship_user2'
    )
    is_active = models.BooleanField(default=True)
    anniversary_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_1} ❤️ {self.user_2}"