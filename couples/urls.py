from django.urls import path
from .views import (
    send_invitation,
    received_invitations,
    accept_invitation,
    reject_invitation,
    couple_status,
    break_up,
    couple_home,
    edit_anniversary,
)

urlpatterns = [
    path('send/', send_invitation, name='send_invitation'),
    path('invitations/', received_invitations, name='received_invitations'),
    path('accept/<int:invitation_id>/', accept_invitation, name='accept_invitation'),
    path('reject/<int:invitation_id>/', reject_invitation, name='reject_invitation'),
    path('status/', couple_status, name='couple_status'),
    path('break/', break_up, name='break_up'),
    path('home/', couple_home, name='couple_home'),
    path('anniversary/edit/', edit_anniversary, name='edit_anniversary'),
]