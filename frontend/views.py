from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.conf import settings
import googlemaps


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
    
    if request.method == "POST":
        pickup_location = request.POST["pickup-location"]
        destination_location = request.POST["destination-location"]
        
        # Get Geocodes 
        gmaps = googlemaps.Client(google_api_key)
        location1 = gmaps.geocode(pickup_location)[0]['geometry']['location']
        location2 = gmaps.geocode(destination_location)[0]['geometry']['location']
        
        # Calculate Distance
        distance_result = gmaps.distance_matrix((location1['lat'], location1['lng']), (location2['lat'], location2['lng']))
        distance = distance_result['rows'][0]['elements'][0]['distance']['value']
        distance_km = distance // 1000 
        
        request.session['distance_km'] = distance_km
        request.session['pickup_location'] = pickup_location
        request.session['destination_location'] = destination_location
        
        return redirect('confirm-delivery')
    
    
    context = {
        'google_api_key': google_api_key
    }
    
    return render(request, 'frontend/book_delivery.html', context)


def confirmDelivery(request):
    
    google_api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
    
    pickup_location = request.session['pickup_location']
    destination_location = request.session['destination_location']
    distance = request.session['distance_km']
    
    price = 2 * distance 


    context = {
        'google_api_key': google_api_key,
        'pickup_location':pickup_location, 
        'destination_location':destination_location,
        'distance':distance, 
        'price':price
    }
    
    return render(request, 'frontend/confirm_delivery.html', context)

    
    


