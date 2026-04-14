import random
import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q

from couples.models import CoupleRelationship
from .models import Place, FavoritePlace, RandomPickHistory
from .forms import PlaceForm

logger = logging.getLogger('wherenow')


def get_partner(user):
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


@login_required
def place_list(request):
    partner = get_partner(request.user)

    if partner:
        places = Place.objects.filter(
            Q(user=request.user) |
            Q(user=partner, shared_with_couple=True)
        ).order_by('-created_at')
    else:
        places = Place.objects.filter(user=request.user).order_by('-created_at')

    logger.info(f'使用者 {request.user.username} 查看地點列表')

    return render(request, 'places/place_list.html', {
        'places': places,
        'partner': partner
    })


@login_required
def place_create(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.user = request.user
            place.save()
            form.save_m2m()

            logger.info(f'使用者 {request.user.username} 新增地點成功：{place.name}')

            return redirect('place_list')
        else:
            logger.warning(f'使用者 {request.user.username} 新增地點失敗：表單驗證未通過')
    else:
        form = PlaceForm()

    return render(request, 'places/place_form.html', {'form': form})


@login_required
def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    partner = get_partner(request.user)

    can_view = False

    if place.user == request.user:
        can_view = True
    elif place.is_public:
        can_view = True
    elif partner and place.user == partner and place.shared_with_couple:
        can_view = True

    if not can_view:
        logger.warning(
            f'使用者 {request.user.username} 嘗試查看無權限地點，地點ID：{pk}'
        )
        raise Http404("你沒有權限查看這個地點")

    can_edit = (place.user == request.user)

    logger.info(
        f'使用者 {request.user.username} 查看地點詳細頁，地點ID：{place.id}，地點名稱：{place.name}'
    )

    return render(request, 'places/place_detail.html', {
        'place': place,
        'can_edit': can_edit,
    })

@login_required
def place_update(request, pk):
    place = get_object_or_404(Place, pk=pk, user=request.user)

    if request.method == 'POST':
        form = PlaceForm(request.POST, instance=place)
        if form.is_valid():
            form.save()

            logger.info(
                f'使用者 {request.user.username} 編輯地點成功，地點ID：{place.id}，地點名稱：{place.name}'
            )

            return redirect('place_detail', pk=place.pk)
        else:
            logger.warning(
                f'使用者 {request.user.username} 編輯地點失敗，地點ID：{place.id}'
            )
    else:
        form = PlaceForm(instance=place)

        logger.info(
            f'使用者 {request.user.username} 進入編輯地點頁面，地點ID：{place.id}'
        )

    return render(request, 'places/place_form.html', {'form': form})


@login_required
def place_delete(request, pk):
    place = get_object_or_404(Place, pk=pk, user=request.user)

    if request.method == 'POST':
        place_name = place.name
        place_id = place.id
        place.delete()

        logger.info(
            f'使用者 {request.user.username} 刪除地點成功，地點ID：{place_id}，地點名稱：{place_name}'
        )

        return redirect('place_list')

    return render(request, 'places/place_confirm_delete.html', {'place': place})


@login_required
def add_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id, is_public=True)

    if place.user != request.user:
        favorite, created = FavoritePlace.objects.get_or_create(
            user=request.user,
            place=place
        )

        if created:
            logger.info(
                f'使用者 {request.user.username} 收藏地點成功，地點ID：{place.id}，地點名稱：{place.name}'
            )
        else:
            logger.warning(
                f'使用者 {request.user.username} 重複收藏地點，地點ID：{place.id}，地點名稱：{place.name}'
            )

    return redirect('place_detail', pk=place.id)


@login_required
def remove_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    favorite = FavoritePlace.objects.filter(user=request.user, place=place)
    deleted_count, _ = favorite.delete()

    if deleted_count > 0:
        logger.info(
            f'使用者 {request.user.username} 取消收藏成功，地點ID：{place.id}，地點名稱：{place.name}'
        )
    else:
        logger.warning(
            f'使用者 {request.user.username} 嘗試取消不存在的收藏，地點ID：{place.id}'
        )

    return redirect('favorite_list')


@login_required
def favorite_list(request):
    favorites = FavoritePlace.objects.filter(user=request.user).select_related('place')

    logger.info(f'使用者 {request.user.username} 查看收藏地點列表')

    return render(request, 'places/favorite_list.html', {'favorites': favorites})


@login_required
def random_pick(request):
    picked_place = None
    error = None

    if request.method == 'POST':
        partner = get_partner(request.user)

        if partner:
            places = Place.objects.filter(
                Q(user=request.user) |
                Q(user=partner, shared_with_couple=True)
            )
        else:
            places = Place.objects.filter(user=request.user)

        if not places.exists():
            error = '目前沒有可供抽選的地點，請先新增地點。'
            logger.warning(f'使用者 {request.user.username} 抽選地點失敗：沒有可抽選地點')
        else:
            picked_place = random.choice(list(places))

            RandomPickHistory.objects.create(
                user=request.user,
                place=picked_place
            )

            logger.info(
                f'使用者 {request.user.username} 隨機抽選地點成功，地點ID：{picked_place.id}，地點名稱：{picked_place.name}'
            )

    return render(request, 'places/random_pick.html', {
        'picked_place': picked_place,
        'error': error
    })


@login_required
def random_pick_history(request):
    histories = RandomPickHistory.objects.filter(user=request.user).select_related('place').order_by('-picked_at')

    logger.info(f'使用者 {request.user.username} 查看隨機抽選紀錄')

    return render(request, 'places/random_pick_history.html', {
        'histories': histories
    })