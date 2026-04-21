from datetime import date
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import CoupleInvitationForm
from .models import CoupleInvitation, CoupleRelationship
from places.models import Place
from memories.models import Memory

logger = logging.getLogger('wherenow')


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
    users = []

    keyword = request.GET.get('q')

    # 🔍 搜尋使用者
    if keyword:
        users = User.objects.filter(
            Q(username__icontains=keyword) |
            Q(email__icontains=keyword)
        ).exclude(id=request.user.id)

    # 📩 發送邀請
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')

        try:
            receiver = User.objects.get(id=receiver_id)

            if receiver == request.user:
                message = '不能邀請自己。'

            else:
                my_relationship_exists = CoupleRelationship.objects.filter(
                    Q(user_1=request.user) | Q(user_2=request.user),
                    is_active=True
                ).exists()

                receiver_relationship_exists = CoupleRelationship.objects.filter(
                    Q(user_1=receiver) | Q(user_2=receiver),
                    is_active=True
                ).exists()

                if my_relationship_exists:
                    message = '你目前已經有情侶關係。'

                elif receiver_relationship_exists:
                    message = '對方目前已有情侶關係。'

                else:
                    invitation_exists = CoupleInvitation.objects.filter(
                        sender=request.user,
                        receiver=receiver,
                        status='pending'
                    ).exists()

                    if invitation_exists:
                        message = '邀請已經送出。'
                    else:
                        CoupleInvitation.objects.create(
                            sender=request.user,
                            receiver=receiver
                        )
                        message = '邀請已送出！'

        except User.DoesNotExist:
            message = '找不到使用者。'

    return render(request, 'couples/send_invitation.html', {
        'users': users,
        'message': message,
        'keyword': keyword
    })


@login_required
def received_invitations(request):
    invitations = CoupleInvitation.objects.filter(
        receiver=request.user,
        status='pending'
    ).order_by('-created_at')

    logger.info(f'使用者 {request.user.username} 查看收到的情侶邀請列表')

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
        logger.warning(
            f'使用者 {request.user.username} 接受邀請失敗：雙方其中一人已有情侶關係'
        )
        return redirect('received_invitations')

    invitation.status = 'accepted'
    invitation.save()

    logger.info(
        f'使用者 {request.user.username} 接受來自 {invitation.sender.username} 的情侶邀請'
    )

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

        logger.info(
            f'使用者 {request.user.username} 與 {invitation.sender.username} 建立情侶關係成功'
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

    logger.info(
        f'使用者 {request.user.username} 拒絕來自 {invitation.sender.username} 的情侶邀請'
    )

    return redirect('received_invitations')


@login_required
def couple_status(request):
    relationship, partner = get_relationship_and_partner(request.user)

    logger.info(f'使用者 {request.user.username} 查看情侶狀態頁面')

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

        if partner:
            logger.info(
                f'使用者 {request.user.username} 與 {partner.username} 結束情侶關係'
            )
        else:
            logger.info(f'使用者 {request.user.username} 結束情侶關係')

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

    logger.info(f'使用者 {request.user.username} 查看情侶首頁')

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
        logger.warning(f'使用者 {request.user.username} 嘗試編輯紀念日，但目前沒有情侶關係')
        return redirect('couple_status')

    if request.method == 'POST':
        anniversary_date = request.POST.get('anniversary_date')
        relationship.anniversary_date = anniversary_date or None
        relationship.save()

        logger.info(
            f'使用者 {request.user.username} 更新紀念日為 {relationship.anniversary_date}'
        )

        return redirect('couple_home')

    logger.info(f'使用者 {request.user.username} 進入編輯紀念日頁面')

    return render(request, 'couples/edit_anniversary.html', {
        'relationship': relationship,
        'partner': partner
    })