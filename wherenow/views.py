from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from places.models import Category, Place
from memories.models import Memory
from couples.models import CoupleRelationship


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


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('/accounts/login/')


@login_required
def home(request):
    categories = Category.objects.all().order_by('name')

    return render(request, 'home.html', {
        'categories': categories
    })


@login_required
def explore_page(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    area = request.GET.get('area', '').strip()
    budget_min = request.GET.get('budget_min', '').strip()
    budget_max = request.GET.get('budget_max', '').strip()

    partner = get_partner(request.user)

    # 地點：公開 / 自己 / 情侶共享
    place_visibility_filter = Q(is_public=True) | Q(user=request.user)
    if partner:
        place_visibility_filter |= Q(user=partner, shared_with_couple=True)

    places = Place.objects.filter(place_visibility_filter).select_related(
        'user', 'category'
    )

    # 回憶：公開 / 自己 / 情侶共享
    memory_visibility_filter = Q(is_public=True) | Q(user=request.user)
    if partner:
        memory_visibility_filter |= Q(user=partner, shared_with_couple=True)

    memories = Memory.objects.filter(memory_visibility_filter).select_related(
        'user', 'place', 'place__category'
    ).prefetch_related('photos')

    # 關鍵字搜尋
    if query:
        places = places.filter(
            Q(name__icontains=query) |
            Q(area__icontains=query) |
            Q(address__icontains=query) |
            Q(note__icontains=query) |
            Q(user__username__icontains=query)
        )

        memories = memories.filter(
            Q(place__name__icontains=query) |
            Q(place__area__icontains=query) |
            Q(comment__icontains=query) |
            Q(user__username__icontains=query)
        )

    # 分類
    if category:
        places = places.filter(category__id=category)
        memories = memories.filter(place__category__id=category)

    # 地區
    if area:
        places = places.filter(area__icontains=area)
        memories = memories.filter(place__area__icontains=area)

    # 最低預算
    if budget_min:
        try:
            budget_min_value = int(budget_min)
            places = places.filter(budget__gte=budget_min_value)
            memories = memories.filter(place__budget__gte=budget_min_value)
        except ValueError:
            pass

    # 最高預算
    if budget_max:
        try:
            budget_max_value = int(budget_max)
            places = places.filter(budget__lte=budget_max_value)
            memories = memories.filter(place__budget__lte=budget_max_value)
        except ValueError:
            pass

    items = []

    for place in places:
        if place.user == request.user:
            visibility_text = '我的地點'
        elif partner and place.user == partner and place.shared_with_couple:
            visibility_text = '情侶共享地點'
        else:
            visibility_text = '公開地點'

        items.append({
            'type': 'place',
            'id': place.id,
            'title': place.name,
            'image_url': place.image.url if place.image else '',
            'username': place.user.username,
            'category': place.category.name if place.category else '未分類',
            'area': place.area or '未填寫',
            'budget': place.budget,
            'summary': place.note if place.note else '這個地點尚未填寫備註。',
            'created_at': place.created_at,
            'detail_url': f'/places/{place.id}/',
            'tag_text': visibility_text,
        })

    for memory in memories:
        first_photo = memory.photos.first()

        if memory.user == request.user:
            visibility_text = '我的回憶'
        elif partner and memory.user == partner and memory.shared_with_couple:
            visibility_text = '情侶共享回憶'
        else:
            visibility_text = '公開回憶'

        items.append({
            'type': 'memory',
            'id': memory.id,
            'title': memory.place.name,
            'image_url': first_photo.image.url if first_photo else '',
            'username': memory.user.username,
            'category': memory.place.category.name if memory.place.category else '未分類',
            'area': memory.place.area or '未填寫',
            'budget': memory.place.budget,
            'summary': memory.comment if memory.comment else '這則回憶尚未填寫心得。',
            'created_at': memory.created_at,
            'detail_url': f'/memories/{memory.id}/',
            'tag_text': visibility_text,
        })

    items.sort(key=lambda x: x['created_at'], reverse=True)

    categories = Category.objects.all().order_by('name')

    return render(request, 'explore.html', {
        'items': items,
        'categories': categories,
        'query': query,
        'selected_category': category,
        'area': area,
        'budget_min': budget_min,
        'budget_max': budget_max,
    })