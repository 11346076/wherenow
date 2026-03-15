from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

def home(request):
    return HttpResponse("Welcome to WhereNow")

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'users/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'nickname': request.user.username}
    )

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
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})