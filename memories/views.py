import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404

from .models import Memory, MemoryPhoto
from places.models import Place, Category
from couples.models import CoupleRelationship

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


def can_view_memory(user, memory):
    partner = get_partner(user)

    if memory.user == user:
        return True

    if partner and memory.user == partner and memory.shared_with_couple:
        return True

    if memory.is_public:
        return True

    return False


@login_required
def memory_list(request):
    memories = Memory.objects.filter(
        user=request.user
    ).order_by('-created_at')

    logger.info(f'使用者 {request.user.username} 查看自己的回憶列表')

    return render(request, 'memories/memory_list.html', {
        'memories': memories,
        'partner': get_partner(request.user),
        'is_shared_view': False,
    })

@login_required
def shared_memory_list(request):
    partner = get_partner(request.user)

    if not partner:
        logger.warning(f'使用者 {request.user.username} 嘗試查看共享回憶，但目前沒有情侶對象')
        return redirect('memory_list')

    memories = Memory.objects.filter(
        Q(user=request.user, shared_with_couple=True) |
        Q(user=partner, shared_with_couple=True)
    ).order_by('-created_at')

    logger.info(f'使用者 {request.user.username} 查看與 {partner.username} 的共享回憶列表')

    return render(request, 'memories/memory_list.html', {
        'memories': memories,
        'partner': partner,
        'is_shared_view': True,
    })


@login_required
def memory_detail(request, pk):
    memory = get_object_or_404(Memory, pk=pk)

    if not can_view_memory(request.user, memory):
        logger.warning(
            f'使用者 {request.user.username} 嘗試查看無權限的回憶，回憶ID：{pk}'
        )
        raise Http404("你沒有權限查看這個回憶")

    photos = memory.photos.all()

    logger.info(
        f'使用者 {request.user.username} 查看回憶詳細頁，回憶ID：{memory.id}'
    )

    return render(request, 'memories/memory_detail.html', {
        'memory': memory,
        'photos': photos,
    })


@login_required
def memory_create(request):
    if request.method == 'POST':
        try:
            place_id = request.POST.get('place')
            place = Place.objects.get(id=place_id, user=request.user)

            memory = Memory.objects.create(
                user=request.user,
                place=place,
                visit_date=request.POST.get('visit_date'),
                comment=request.POST.get('comment'),
                rating=request.POST.get('rating') or 0,
                cost=request.POST.get('cost') or 0,
                recommended=bool(request.POST.get('recommended')),
                shared_with_couple=bool(request.POST.get('shared_with_couple')),
                is_public=bool(request.POST.get('is_public')),
            )

            image_count = 0
            for image in request.FILES.getlist('images'):
                MemoryPhoto.objects.create(
                    memory=memory,
                    image=image
                )
                image_count += 1

            logger.info(
                f'使用者 {request.user.username} 新增回憶成功，回憶ID：{memory.id}，地點：{place.name}，照片數：{image_count}'
            )

            return redirect('memory_detail', pk=memory.pk)

        except Place.DoesNotExist:
            logger.warning(
                f'使用者 {request.user.username} 新增回憶失敗：找不到地點 ID {request.POST.get("place")}'
            )
            raise Http404("找不到對應地點")

        except Exception as e:
            logger.exception(
                f'使用者 {request.user.username} 新增回憶時發生系統錯誤：{str(e)}'
            )
            raise

    places = Place.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'memories/memory_create.html', {
        'places': places
    })


@login_required
def memory_edit(request, pk):
    memory = get_object_or_404(Memory, pk=pk, user=request.user)

    if request.method == 'POST':
        try:
            place_id = request.POST.get('place')
            place = Place.objects.get(id=place_id, user=request.user)

            memory.place = place
            memory.visit_date = request.POST.get('visit_date')
            memory.comment = request.POST.get('comment')
            memory.rating = request.POST.get('rating') or 0
            memory.cost = request.POST.get('cost') or 0
            memory.recommended = bool(request.POST.get('recommended'))
            memory.shared_with_couple = bool(request.POST.get('shared_with_couple'))
            memory.is_public = bool(request.POST.get('is_public'))
            memory.save()

            image_count = 0
            for image in request.FILES.getlist('images'):
                MemoryPhoto.objects.create(
                    memory=memory,
                    image=image
                )
                image_count += 1

            logger.info(
                f'使用者 {request.user.username} 編輯回憶成功，回憶ID：{memory.id}，新增照片數：{image_count}'
            )

            return redirect('memory_detail', pk=memory.pk)

        except Place.DoesNotExist:
            logger.warning(
                f'使用者 {request.user.username} 編輯回憶失敗：找不到地點 ID {request.POST.get("place")}'
            )
            raise Http404("找不到對應地點")

        except Exception as e:
            logger.exception(
                f'使用者 {request.user.username} 編輯回憶時發生系統錯誤，回憶ID：{memory.id}，錯誤：{str(e)}'
            )
            raise

    places = Place.objects.filter(user=request.user).order_by('-created_at')
    photos = memory.photos.all()

    logger.info(
        f'使用者 {request.user.username} 進入編輯回憶頁面，回憶ID：{memory.id}'
    )

    return render(request, 'memories/memory_edit.html', {
        'memory': memory,
        'places': places,
        'photos': photos,
    })


@login_required
def memory_delete(request, pk):
    memory = get_object_or_404(Memory, pk=pk, user=request.user)

    if request.method == 'POST':
        memory_id = memory.id
        place_name = memory.place.name if memory.place else '未知地點'

        memory.delete()

        logger.info(
            f'使用者 {request.user.username} 刪除回憶成功，回憶ID：{memory_id}，地點：{place_name}'
        )

        return redirect('memory_list')

    logger.info(
        f'使用者 {request.user.username} 進入刪除回憶頁面，回憶ID：{memory.id}'
    )

    return render(request, 'memories/memory_delete.html', {
        'memory': memory
    })


@login_required
def memory_photo_delete(request, pk):
    photo = get_object_or_404(MemoryPhoto, pk=pk, memory__user=request.user)
    memory_id = photo.memory.id

    if request.method == 'POST':
        photo_id_value = photo.id
        photo.delete()

        logger.info(
            f'使用者 {request.user.username} 刪除回憶照片成功，照片ID：{photo_id_value}，回憶ID：{memory_id}'
        )

        return redirect('memory_edit', pk=memory_id)

    logger.info(
        f'使用者 {request.user.username} 進入刪除照片頁面，照片ID：{photo.id}，回憶ID：{memory_id}'
    )

    return render(request, 'memories/memory_photo_delete.html', {
        'photo': photo
    })


@login_required
def public_memory_search(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    area = request.GET.get('area', '').strip()
    budget_min = request.GET.get('budget_min', '').strip()
    budget_max = request.GET.get('budget_max', '').strip()

    memories = Memory.objects.filter(is_public=True).select_related(
        'user', 'place', 'place__category'
    ).prefetch_related('photos')

    if query:
        memories = memories.filter(
            Q(place__name__icontains=query) |
            Q(place__area__icontains=query) |
            Q(comment__icontains=query) |
            Q(user__username__icontains=query)
        )

    if category:
        memories = memories.filter(place__category__id=category)

    if area:
        memories = memories.filter(place__area__icontains=area)

    if budget_min:
        try:
            memories = memories.filter(place__budget__gte=int(budget_min))
        except ValueError:
            pass

    if budget_max:
        try:
            memories = memories.filter(place__budget__lte=int(budget_max))
        except ValueError:
            pass

    memories = memories.order_by('-created_at')
    categories = Category.objects.all().order_by('name')

    return render(request, 'memories/public_search.html', {
        'memories': memories,
        'query': query,
        'categories': categories,
        'selected_category': category,
        'area': area,
        'budget_min': budget_min,
        'budget_max': budget_max,
    })