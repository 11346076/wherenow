from django.urls import path
from .views import send_invitation, received_invitations, accept_invitation, reject_invitation

urlpatterns = [
    path('send/', send_invitation, name='send_invitation'),
    path('invitations/', received_invitations, name='received_invitations'),
    path('accept/<int:invitation_id>/', accept_invitation, name='accept_invitation'),
    path('reject/<int:invitation_id>/', reject_invitation, name='reject_invitation'),
]