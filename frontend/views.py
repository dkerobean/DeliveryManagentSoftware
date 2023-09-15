from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
import googlemaps
import math
from .models import BookDelivery, Contact, DeliveryAction, DeliveryType
from django.contrib.auth.models import AnonymousUser
from admin_dashboard.models import DeliveryMultiplier


""" HOME PAGE """


def homePage(request):

    return render(request, 'frontend/index.html')


"""CONTACT PAGE"""


def contactPage(request):

    if request.method == "POST":
        topic = request.POST["topic"]
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        message = request.POST["message"]

        contact = Contact(topic=topic, name=name, email=email,
                          phone=phone, message=message)
        contact.save()
        messages.success(request, "Message Sent Successfully")
        return redirect('home')

    return render(request, 'frontend/contact.html')


""" USER AUTH PAGES """


def userLogin(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged In')
            return redirect(request.GET.get('next', 'book-delivery'))

        else:
            messages.error(request, 'Username or password incorrect')
            return redirect('user-login')

    return render(request, 'frontend/auth/login.html')


def userLogout(request):

    logout(request)
    return redirect('home')

    return render(request, 'frontend/auth/login.html')


def userSignUp(request):

    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request, 'Registration Success')
            login(request, user)
        else:
            messages.error(request, 'Registration Failure')
            return redirect('user-register')

    context = {
        'form': form
    }

    return render(request, 'frontend/auth/register.html', context)


""" 404 PAGE """


def handler404(request, exception):

    return render(request, 'frontend/404.html', status=404)


""" BOOK DELIVERY """


@login_required(login_url="user-login")
def bookDelivery(request):

    google_api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)

    deliveryAction = DeliveryAction.objects.all()
    deliveryType = DeliveryType.objects.all()

    if request.method == "POST":

        item = request.POST["item"]
        item_type = request.POST["item-type"]
        pickup_location = request.POST["pickup-location"]
        destination_location = request.POST["destination-location"]

        # Get Geocodes
        gmaps = googlemaps.Client(google_api_key)
        location1 = gmaps.geocode(pickup_location)[0]['geometry']['location']
        location2 = gmaps.geocode(destination_location)[0]['geometry']['location'] # noqa

        # Calculate Distance
        distance_result = gmaps.distance_matrix((location1['lat'], location1['lng']), (location2['lat'], location2['lng'])) # noqa

        distance = distance_result['rows'][0]['elements'][0]['distance']['value'] # noqa

        distance_km = round(distance / 1000, 1)

        request.session['distance_km'] = distance_km
        request.session['pickup_location'] = pickup_location
        request.session['destination_location'] = destination_location
        request.session['item'] = item
        request.session['item_type'] = item_type

        return redirect('confirm-delivery')

    context = {
        'google_api_key': google_api_key,
        'deliveryAction': deliveryAction,
        'deliveryType': deliveryType
    }

    return render(request, 'frontend/delivery/book_delivery.html', context)


@login_required(login_url="user-login")
def confirmDelivery(request):

    google_api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)

    # Check if user is autenticated or not
    if not isinstance(request.user, AnonymousUser):
        profile = request.user.profile
    else:
        profile = ''

    pickup_location = request.session['pickup_location']
    destination_location = request.session['destination_location']
    distance = request.session['distance_km']
    item = request.session['item']
    item_type = request.session['item_type']

    # Calculate price of delivery
    multiplier = DeliveryMultiplier.objects.first()

    # Convert the multiplier to a float
    multiplier_value = float(multiplier.multiplier)

    price = math.ceil(multiplier_value * distance)

    if request.method == "POST":
        sender_contact = request.POST['sender_contact']
        reciever_contact = request.POST['reciever_contact']

        delivery_details = BookDelivery(profile=profile, item=item,
                                        item_type=item_type,
                                        pickup_location=pickup_location,
                                        destination_location=destination_location, # noqa
                                        sender_contact=sender_contact,
                                        reciever_contact=reciever_contact,
                                        price=price)
        delivery_details.save()
        messages.success(request, 'Delivery Booked, You Will Recieve A Call')
        return redirect('home')

    context = {
        'google_api_key': google_api_key,
        'pickup_location': pickup_location,
        'destination_location': destination_location,
        'distance': distance,
        'price': price
    }

    return render(request, 'frontend/delivery/confirm_delivery.html', context)


""" TRACK ORDER """


def trackOrder(request):

    status = None

    if request.method == "POST":
        order_number = request.POST['order-number']

        try:
            order = BookDelivery.objects.get(order_number=order_number)
            status = order.order_status
        except BookDelivery.DoesNotExist:
            status = None

        request.session['status'] = str(status)

        return redirect('order-results')

    return render(request, 'frontend/track_order/track_order.html')


def orderResults(request):

    order_status = request.session['status']

    context = {
        'order_status': order_status
    }

    return render(request, 'frontend/track_order/order_results.html', context)
