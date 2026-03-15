from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CoupleInvitationForm
from django.shortcuts import get_object_or_404
from .models import CoupleInvitation, CoupleRelationship


@login_required
def send_invitation(request):
    message = ''

    if request.method == 'POST':
        form = CoupleInvitationForm(request.POST)
        if form.is_valid():
            receiver_username = form.cleaned_data['receiver_username']

            if receiver_username == request.user.username:
                message = '不能邀請自己。'
            else:
                try:
                    receiver = User.objects.get(username=receiver_username)

                    invitation_exists = CoupleInvitation.objects.filter(
                        sender=request.user,
                        receiver=receiver,
                        status='pending'
                    ).exists()

                    if invitation_exists:
                        message = '邀請已經送出，請勿重複邀請。'
                    else:
                        CoupleInvitation.objects.create(
                            sender=request.user,
                            receiver=receiver,
                            status='pending'
                        )
                        message = '邀請已送出。'

                except User.DoesNotExist:
                    message = '找不到這個帳號。'
    else:
        form = CoupleInvitationForm()

    return render(request, 'couples/send_invitation.html', {
        'form': form,
        'message': message
    })

@login_required
def received_invitations(request):

    invitations = CoupleInvitation.objects.filter(
        receiver=request.user,
        status='pending'
    )

    return render(request, 'couples/received_invitations.html', {
        'invitations': invitations
    })


@login_required
def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(
        CoupleInvitation,
        id=invitation_id,
        receiver=request.user,
        status='pending'
    )

    invitation.status = 'accepted'
    invitation.save()

    relationship_exists = CoupleRelationship.objects.filter(
        user_1=invitation.sender,
        user_2=request.user
    ).exists() or CoupleRelationship.objects.filter(
        user_1=request.user,
        user_2=invitation.sender
    ).exists()

    if not relationship_exists:
        CoupleRelationship.objects.create(
            user_1=invitation.sender,
            user_2=request.user,
            is_active=True
        )

    return redirect('received_invitations')

@login_required
def reject_invitation(request, invitation_id):
    invitation = get_object_or_404(
        CoupleInvitation,
        id=invitation_id,
        receiver=request.user,
        status='pending'
    )

    invitation.status = 'rejected'
    invitation.save()

    return redirect('received_invitations')