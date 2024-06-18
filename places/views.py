# places/views.py
from django.shortcuts import render
from .models import Place

def index(request):
    places = Place.objects.all()
    return render(request, 'places/index.html', {'places': places})

def place_detail(request, place_id):
    place = Place.objects.get(id=place_id)
    return render(request, 'places/detail.html', {'place': place})

