import logging

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404

from .forms import MemoryForm, MemoryPhotoInlineFormset
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
        memory_form = MemoryForm(request.POST, request.FILES, user=request.user)
        photo_formset = MemoryPhotoInlineFormset(request.POST, request.FILES, instance=Memory(user=request.user))

        if memory_form.is_valid() and photo_formset.is_valid():
            try:
                with transaction.atomic():
                    memory = memory_form.save(commit=False)
                    memory.user = request.user
                    memory.save()
                    photo_formset.instance = memory
                    photo_formset.save()

                    logger.info(
                        f'使用者 {request.user.username} 新增回憶成功，回憶ID：{memory.id}，照片數：{photo_formset.total_form_count()}'
                    )

                    return redirect('memory_detail', pk=memory.pk)

            except Exception as e:
                logger.exception(
                    f'使用者 {request.user.username} 新增回憶時發生系統錯誤：{str(e)}'
                )
                raise
    else:
        memory_form = MemoryForm(user=request.user)
        photo_formset = MemoryPhotoInlineFormset(instance=Memory(user=request.user))

    return render(request, 'memories/memory_create.html', {
        'memory_form': memory_form,
        'photo_formset': photo_formset
    })


@login_required
def memory_edit(request, pk):
    memory = get_object_or_404(Memory, pk=pk, user=request.user)

    if request.method == 'POST':
        memory_form = MemoryForm(request.POST, request.FILES, instance=memory, user=request.user)
        photo_formset = MemoryPhotoInlineFormset(request.POST, request.FILES, instance=memory)

        if memory_form.is_valid() and photo_formset.is_valid():
            try:
                with transaction.atomic():
                    memory_form.save()
                    photo_formset.save()

                    logger.info(
                        f'使用者 {request.user.username} 編輯回憶成功，回憶ID：{memory.id}，照片數：{photo_formset.total_form_count()}'
                    )

                    return redirect('memory_detail', pk=memory.pk)

            except Exception as e:
                logger.exception(
                    f'使用者 {request.user.username} 編輯回憶時發生系統錯誤，回憶ID：{memory.id}，錯誤：{str(e)}'
                )
                raise
    else:
        memory_form = MemoryForm(instance=memory, user=request.user)
        photo_formset = MemoryPhotoInlineFormset(instance=memory)

    photos = memory.photos.all()

    logger.info(
        f'使用者 {request.user.username} 進入編輯回憶頁面，回憶ID：{memory.id}'
    )

    return render(request, 'memories/memory_edit.html', {
        'memory': memory,
        'memory_form': memory_form,
        'photo_formset': photo_formset,
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