from math import radians, sin, cos, sqrt, atan2
from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.conf import settings


""" HOME PAGE """
def homePage(request):    
    
    return render(request, 'frontend/index.html')


""" USER AUTH PAGES """

def userLogin(request):    
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        try:
            user = User.ogjects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged In')
            return redirect('home')
        else:
            messages.error(request, 'Username or password incorrect')
    
    
    return render(request, 'frontend/login.html')


def userLogout(request):
    logout(request)
    return redirect('home')

    return render(request, 'frontend/login.html')


def userSignUp(request):
    
    form = CustomUserCreationForm()
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request, 'Registration Success')
            login(request, user)
        return redirect('home')
    
    context = {
        'form':form
    }
    
    return render(request, 'frontend/register.html', context)


""" 404 PAGE """

def handler404(request, exception):
    
    return render(request, 'frontend/404.html', status=404)


""" BOOK DELIVERY """

def bookDelivery(request):
    
    google_api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
    
    if request.method == 'POST':
        
        pickup_location = request.POST.get('pickup-location')
        destination_location = request.POST.get('destination-location')
        
        # Getting Geocode Data For The Two Locations 
        geocoding_url1 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + \
            location1 + '&key=' + google_api_key
        geocoding_response1 = requests.get(geocoding_url1)
        geocoding_data1 = geocoding_response1.json()

        geocoding_url2 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + \
            location2 + '&key=' + google_api_key
        geocoding_response2 = requests.get(geocoding_url2)
        geocoding_data2 = geocoding_response2.json()
        
        # Get the latitude and longitude of the two locations
        location1_lat = geocoding_data1['results'][0]['geometry']['pickup-location']['lat']
        location1_lng = geocoding_data1['results'][0]['geometry']['pickup-location']['lng']
        
        location2_lat = geocoding_data2['results'][0]['geometry']['destination-location']['lat']
        location2_lng = geocoding_data2['results'][0]['geometry']['destination-location']['lng']
    
    context = {
        'google_api_key': google_api_key
    }
    
    return render(request, 'frontend/book_delivery.html', context)



