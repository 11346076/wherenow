from django.shortcuts import render, redirect, get_object_or_404
from .models import Memory, MemoryPhoto
from places.models import Place
from django.contrib.auth.decorators import login_required


def memory_list(request):
    memories = Memory.objects.all().order_by('-created_at')
    return render(request, 'memories/memory_list.html', {'memories': memories})


def memory_detail(request, pk):
    memory = get_object_or_404(Memory, pk=pk)
    photos = memory.photos.all()
    return render(request, 'memories/memory_detail.html', {
        'memory': memory,
        'photos': photos,
    })


@login_required
def memory_create(request):
    if request.method == 'POST':
        place_id = request.POST.get('place')
        place = Place.objects.get(id=place_id)

        memory = Memory.objects.create(
            user=request.user,
            place=place,
            visit_date=request.POST.get('visit_date'),
            comment=request.POST.get('comment'),
            rating=request.POST.get('rating') or 0,
            cost=request.POST.get('cost') or 0,
            recommended=True if request.POST.get('recommended') else False,
        )

        for image in request.FILES.getlist('images'):
            MemoryPhoto.objects.create(
                memory=memory,
                image=image
            )

        return redirect('memory_detail', pk=memory.pk)

    places = Place.objects.all()
    return render(request, 'memories/memory_create.html', {'places': places})

@login_required
def memory_delete(request, pk):
    memory = get_object_or_404(Memory, pk=pk)

    if request.method == 'POST':
        memory.delete()
        return redirect('memory_list')

    return render(request, 'memories/memory_delete.html', {'memory': memory})

@login_required
def memory_edit(request, pk):
    memory = get_object_or_404(Memory, pk=pk)

    if request.method == 'POST':
        place_id = request.POST.get('place')
        memory.place = Place.objects.get(id=place_id)
        memory.visit_date = request.POST.get('visit_date')
        memory.comment = request.POST.get('comment')
        memory.rating = request.POST.get('rating') or 0
        memory.cost = request.POST.get('cost') or 0
        memory.recommended = True if request.POST.get('recommended') else False
        memory.save()

        for image in request.FILES.getlist('images'):
            MemoryPhoto.objects.create(
                memory=memory,
                image=image
            )

        return redirect('memory_detail', pk=memory.pk)

    places = Place.objects.all()
    photos = memory.photos.all()
    return render(request, 'memories/memory_edit.html', {
        'memory': memory,
        'places': places,
        'photos': photos,
    })

@login_required
def memory_photo_delete(request, photo_id):
    photo = get_object_or_404(MemoryPhoto, pk=photo_id)
    memory_id = photo.memory.id

    if request.method == 'POST':
        photo.delete()
        return redirect('memory_edit', pk=memory_id)

    return render(request, 'memories/memory_photo_delete.html', {'photo': photo})