from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse

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