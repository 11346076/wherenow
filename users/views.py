from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from .forms import (
    ProfileForm,
    CustomLoginForm,
    RegisterForm,
)

from places.models import Place, FavoritePlace
from memories.models import Memory
from couples.utils import get_partner


def _google_login_available():
    google = settings.SOCIALACCOUNT_PROVIDERS.get('google', {})
    app = google.get('APP', {})
    return bool(app.get('client_id') and app.get('secret'))


def custom_login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = CustomLoginForm(
            data=request.POST,
            request=request
        )

        if form.is_valid():
            return form.login(
                request,
                redirect_url='/home/'
            )

    else:
        form = CustomLoginForm(
            request=request
        )

    return render(request, 'account/login.html', {
        'form': form,
        'has_google_login': _google_login_available(),
    })


def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.email = form.cleaned_data.get('email')

            user.save()

            messages.success(
                request,
                '註冊成功，請登入。'
            )

            return redirect('account_login')

    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {
        'form': form
    })


@login_required
def profile(request):

    user = request.user

    partner = get_partner(user)

    place_count = Place.objects.filter(
        user=user
    ).count()

    memory_count = Memory.objects.filter(
        user=user
    ).count()

    favorite_count = FavoritePlace.objects.filter(
        user=user
    ).count()

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

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect('profile')

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(request, 'users/edit_profile.html', {
        'form': form
    })