from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from places.models import Place, FavoritePlace
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


@login_required
def profile(request):
    user = request.user
    partner = get_partner(user)

    place_count = Place.objects.filter(user=user).count()
    memory_count = Memory.objects.filter(user=user).count()
    favorite_count = FavoritePlace.objects.filter(user=user).count()

    return render(request, 'users/profile.html', {
        'place_count': place_count,
        'memory_count': memory_count,
        'favorite_count': favorite_count,
        'partner': partner,
    })


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {
        'form': form
    })