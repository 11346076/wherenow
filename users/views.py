import logging

from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile

logger = logging.getLogger('wherenow')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            logger.info(f'新使用者註冊成功：{user.username}')

            return redirect('login')
        else:
            logger.warning('使用者註冊失敗：表單驗證未通過')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def home(request):
    return render(request, 'home.html')


@login_required
def profile_view(request):
    profile = request.user.profile

    logger.info(f'使用者 {request.user.username} 查看個人資料')

    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'nickname': request.user.username}
    )

    if created:
        logger.info(f'系統自動建立使用者 {request.user.username} 的 Profile')

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()

            logger.info(f'使用者 {request.user.username} 更新個人資料成功')

            return redirect('profile')
        else:
            logger.warning(f'使用者 {request.user.username} 更新個人資料失敗：表單驗證未通過')

    else:
        form = ProfileForm(instance=profile)

        logger.info(f'使用者 {request.user.username} 進入編輯個人資料頁面')

    return render(request, 'users/edit_profile.html', {'form': form})