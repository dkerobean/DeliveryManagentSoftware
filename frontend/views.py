from math import radians, sin, cos, sqrt, atan2
from django.shortcuts import render
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
    
    
    context = {
        'google_api_key': google_api_key
    }
    
    return render(request, 'frontend/book_delivery.html', context)


def confirmDelivery(request):
    
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

        # Calculate the distance between the two locations
        distance_m = distance(location1_lat, location1_lng,
                              location2_lat, location2_lng)

        # Create a map centered on the first location, with a marker for both locations
        map_url = 'https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=10&size=600x300&markers=color:red%7C{},{}&markers=color:blue%7C{},{}&key=' + google_api_key.format(
            location1_lat, location1_lng, location1_lat, location1_lng, location2_lat, location2_lng)

    context = {
        'google_api_key': google_api_key,
        'distance_m': distance_m,
        'map_url': map_url
    }
    
    return render(request, 'frontend/confirm_delivery.html', context)

    
    


def my_view(request):
    if request.method == 'POST':
        location1 = request.POST.get('location1')
        location2 = request.POST.get('location2')

        geocoding_url1 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + \
            location1 + '&key=' 
        geocoding_response1 = requests.get(geocoding_url1)
        geocoding_data1 = geocoding_response1.json()

        geocoding_url2 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + \
            location2 + '&key=YOUR_API_KEY'
        geocoding_response2 = requests.get(geocoding_url2)
        geocoding_data2 = geocoding_response2.json()

        # Get the latitude and longitude of the two locations
        location1_lat = geocoding_data1['results'][0]['geometry']['location']['lat']
        location1_lng = geocoding_data1['results'][0]['geometry']['location']['lng']
        location2_lat = geocoding_data2['results'][0]['geometry']['location']['lat']
        location2_lng = geocoding_data2['results'][0]['geometry']['location']['lng']

        # Calculate the distance between the two locations
        distance_m = distance(location1_lat, location1_lng,
                              location2_lat, location2_lng)

        # Create a map centered on the first location, with a marker for both locations
        map_url = 'https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=10&size=600x300&markers=color:red%7C{},{}&markers=color:blue%7C{},{}&key=YOUR_API_KEY'.format(
            location1_lat, location1_lng, location1_lat, location1_lng, location2_lat, location2_lng)

        # Render the template with the distance and map URL
        return render(request, 'my_template.html', {'distance_m': distance_m, 'map_url': map_url})
    else:
        # Render the form template if the request method is not POST
        return render(request, 'my_form_template.html')


def distance(lat1, lon1, lat2, lon2):
    R = 6373.0  # approximate radius of earth in km

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance_km = R * c
    distance_m = distance_km * 1000

    return distance_m
