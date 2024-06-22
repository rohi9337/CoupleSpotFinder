# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import View
from .models import Place
from .forms import PlaceForm
from account.models import UserProfile  # Import UserProfile model

class CustomLoginView(View):
    template_name = 'places/login.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    
    return render(request, 'places/register.html', {'form': form})


def index(request):
    places = Place.objects.all()
    return render(request, 'places/index.html', {'places': places})


@login_required
def create_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save()
            return redirect('place_detail', place.id)
    else:
        form = PlaceForm()
    
    return render(request, 'places/create_place.html', {'form': form})


@login_required
def place_detail(request, place_id):
    place = Place.objects.filter(id=place_id).first()
    if not place:
        return HttpResponseNotFound("Place not found.")
    return render(request, 'places/detail.html', {'place': place})


@login_required
def profile(request):
    user_profile = request.user.userprofile  # Assuming UserProfile is related to User through OneToOneField
    return render(request, 'accounts/profile.html', {'user_profile': user_profile})
