from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Place
from .forms import PlaceForm


@login_required
def place_list(request):
    places = Place.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'places/place_list.html', {'places': places})


@login_required
def place_create(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.user = request.user
            place.save()
            return redirect('place_list')
    else:
        form = PlaceForm()

    return render(request, 'places/place_form.html', {'form': form})


@login_required
def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk, user=request.user)
    return render(request, 'places/place_detail.html', {'place': place})

@login_required
def place_update(request, pk):
    place = get_object_or_404(Place, pk=pk, user=request.user)

    if request.method == 'POST':
        form = PlaceForm(request.POST, instance=place)
        if form.is_valid():
            form.save()
            return redirect('place_detail', pk=place.pk)
    else:
        form = PlaceForm(instance=place)

    return render(request, 'places/place_form.html', {'form': form})

@login_required
def place_delete(request, pk):
    place = get_object_or_404(Place, pk=pk, user=request.user)

    if request.method == 'POST':
        place.delete()
        return redirect('place_list')

    return render(request, 'places/place_confirm_delete.html', {'place': place})