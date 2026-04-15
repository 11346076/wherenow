from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from places.models import Category   # ⭐ 這行要加


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('/accounts/login/')


@login_required
def home(request):
    categories = Category.objects.all().order_by('name')  # ⭐ 新增

    return render(request, 'home.html', {
        'categories': categories   # ⭐ 傳給模板
    })