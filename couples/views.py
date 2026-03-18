from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import CoupleInvitationForm
from .models import CoupleInvitation, CoupleRelationship
from places.models import Place
from memories.models import Memory


def get_relationship_and_partner(user):
    relationship = CoupleRelationship.objects.filter(
        user_1=user,
        is_active=True
    ).first()

    if relationship:
        return relationship, relationship.user_2

    relationship = CoupleRelationship.objects.filter(
        user_2=user,
        is_active=True
    ).first()

    if relationship:
        return relationship, relationship.user_1

    return None, None


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

                    my_relationship_exists = CoupleRelationship.objects.filter(
                        is_active=True,
                        user_1=request.user
                    ).exists() or CoupleRelationship.objects.filter(
                        is_active=True,
                        user_2=request.user
                    ).exists()

                    receiver_relationship_exists = CoupleRelationship.objects.filter(
                        is_active=True,
                        user_1=receiver
                    ).exists() or CoupleRelationship.objects.filter(
                        is_active=True,
                        user_2=receiver
                    ).exists()

                    if my_relationship_exists:
                        message = '你目前已經有情侶關係，不能再次邀請。'
                    elif receiver_relationship_exists:
                        message = '對方目前已經有情侶關係。'
                    else:
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
    ).order_by('-created_at')

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

    sender_has_relationship = CoupleRelationship.objects.filter(
        is_active=True,
        user_1=invitation.sender
    ).exists() or CoupleRelationship.objects.filter(
        is_active=True,
        user_2=invitation.sender
    ).exists()

    receiver_has_relationship = CoupleRelationship.objects.filter(
        is_active=True,
        user_1=request.user
    ).exists() or CoupleRelationship.objects.filter(
        is_active=True,
        user_2=request.user
    ).exists()

    if sender_has_relationship or receiver_has_relationship:
        return redirect('received_invitations')

    invitation.status = 'accepted'
    invitation.save()

    relationship_exists = CoupleRelationship.objects.filter(
        user_1=invitation.sender,
        user_2=request.user,
        is_active=True
    ).exists() or CoupleRelationship.objects.filter(
        user_1=request.user,
        user_2=invitation.sender,
        is_active=True
    ).exists()

    if not relationship_exists:
        CoupleRelationship.objects.create(
            user_1=invitation.sender,
            user_2=request.user,
            is_active=True
        )

    return redirect('couple_status')


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


@login_required
def couple_status(request):
    relationship, partner = get_relationship_and_partner(request.user)

    return render(request, 'couples/couple_status.html', {
        'relationship': relationship,
        'partner': partner
    })


@login_required
def break_up(request):
    relationship, partner = get_relationship_and_partner(request.user)

    if relationship:
        relationship.is_active = False
        relationship.save()

    return redirect('couple_status')


@login_required
def couple_home(request):
    relationship, partner = get_relationship_and_partner(request.user)

    days_together = None
    shared_place_count = 0
    shared_memory_count = 0
    recent_memories = []

    if relationship and partner:
        if relationship.anniversary_date:
            days_together = (date.today() - relationship.anniversary_date).days

        shared_place_count = Place.objects.filter(
            Q(user=request.user, shared_with_couple=True) |
            Q(user=partner, shared_with_couple=True)
        ).count()

        shared_memory_count = Memory.objects.filter(
            Q(user=request.user, shared_with_couple=True) |
            Q(user=partner, shared_with_couple=True)
        ).count()

        recent_memories = Memory.objects.filter(
            Q(user=request.user, shared_with_couple=True) |
            Q(user=partner, shared_with_couple=True)
        ).order_by('-created_at')[:5]

    return render(request, 'couples/couple_home.html', {
        'relationship': relationship,
        'partner': partner,
        'days_together': days_together,
        'shared_place_count': shared_place_count,
        'shared_memory_count': shared_memory_count,
        'recent_memories': recent_memories,
    })


@login_required
def edit_anniversary(request):
    relationship, partner = get_relationship_and_partner(request.user)

    if not relationship:
        return redirect('couple_status')

    if request.method == 'POST':
        anniversary_date = request.POST.get('anniversary_date')
        relationship.anniversary_date = anniversary_date or None
        relationship.save()
        return redirect('couple_home')

    return render(request, 'couples/edit_anniversary.html', {
        'relationship': relationship,
        'partner': partner
    })