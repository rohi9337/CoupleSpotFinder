# places/views.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render,redirect
from .models import Place
from .forms import PlaceForm

def index(request):
    places = Place.objects.all()
    return render(request, 'places/index.html', {'places': places})

@user_passes_test(lambda u: u.is_superuser)
def create_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save()  # Save the form data to create a new Place object
            return redirect('place_detail', place.id)  # Redirect to the detail view of the new place
    else:
        form = PlaceForm()
    
    return render(request, 'places/create_place.html', {'form': form})
    


def place_detail(request, place_id):
    place = Place.objects.get(id=place_id)
    return render(request, 'places/detail.html', {'place': place})

