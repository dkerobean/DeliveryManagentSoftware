from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from frontend.models import BookDelivery, Contact, DeliveryAction, DeliveryType
from .models import DeliveryMultiplier
from .forms import EditDeliveryForm, BookDeliveryForm, AddDeliveryActionForm, AddDeliveryTypeForm
import uuid 
from django.urls import reverse
import googlemaps
from django.conf import settings
import math



# ceck if user has admin status
def is_admin(user):
    return user.is_authenticated and user.is_staff

""" HOME """
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def homePage(request):
    
    orders = BookDelivery.objects.filter(is_deleted=False)
    cancelled = BookDelivery.objects.filter(is_deleted=True)
    pending = BookDelivery.objects.filter(order_status='Pending', is_deleted=False)
    completed = BookDelivery.objects.filter(order_status='Completed')
    
    total_orders = orders.count
    pending_orders = pending.count
    completed_orders = completed.count
    cancelled_orders = cancelled.count
    
    all_messages = Contact.objects.all()
    
    
    context = {
        'all_messages':all_messages,
        'orders': orders,
        'cancelled': cancelled,
        'pending': pending,
        'completed': completed, 
        
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        
    }
    
    return render(request, 'admin_dashboard/index.html', context)


""" AUTENTHICATION """

def loginPage(request):
    
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin-home')
    
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.success(request, 'Logged In')
                return redirect('admin-home')  
              
            login(request, user)
            messages.success(request, 'Logged In')
            return redirect('home')
        
        else:
            messages.error(request, 'Username or password incorrect')

    return render(request, 'admin_dashboard/Auth/login.html')


""" ORDERS """

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def addOrder(request):
    
    form = BookDeliveryForm()
    
    if request.method == 'POST':
        form = BookDeliveryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order created successfully')
            return redirect('all-orders')
        
    context = {
        'form':form
    }
    
    
    return render(request, 'admin_dashboard/Orders/addOrder.html', context)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def allOrders(request):
    
    orders = BookDelivery.objects.filter(is_deleted=False)
    cancelled = BookDelivery.objects.filter(is_deleted=True)
    pending = BookDelivery.objects.filter(order_status='Pending', is_deleted=False)
    completed = BookDelivery.objects.filter(order_status='Completed')
    
    # add order 
    form = BookDeliveryForm()
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Order created successfully')
            return redirect('all-orders')
        
    context = {
        'orders':orders, 
        'form':form, 
        'cancelled':cancelled, 
        'pending':pending, 
        'completed':completed
    }
    
    return render(request, 'admin_dashboard/Orders/viewAll.html', context)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def orderDetails(request, pk):
    
    order = BookDelivery.objects.get(id=(pk))
    
    # get number of rides
    rider = order.rider
    assigned_rides = None
    if rider: 
        assigned_rides = rider.rider.count()
    
    
    context = {
        'order':order, 
        'assigned_rides': assigned_rides
    }
    
    return render(request, 'admin_dashboard/Orders/orderDetails.html', context)

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def editOrder(request, pk):
    
    google_api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
    
    order = BookDelivery.objects.get(id=pk)
    form = EditDeliveryForm(instance=order)
    
    if request.method == "POST":
        form = EditDeliveryForm(request.POST, instance=order)
        if form.is_valid():
            
            data = form.save(commit=False)
            
            # Get Geocodes 
            gmaps = googlemaps.Client(google_api_key)
            location1 = gmaps.geocode(form.instance.pickup_location)[
                0]['geometry']['location']
            location2 = gmaps.geocode(form.instance.destination_location)[0]['geometry']['location']
        
            # Calculate Distance
            distance_result = gmaps.distance_matrix((location1['lat'], location1['lng']), (location2['lat'], location2['lng']))
            distance = distance_result['rows'][0]['elements'][0]['distance']['value']
            distance_km = distance // 1000
            
            #price of delivery
            multiplier = DeliveryMultiplier.objects.all()
            form.instance.price = math.ceil(2 * distance_km)
        
            data.save()
            messages.success(request, "Order edited successfully")
            #url = reverse('order-details', kwargs={'pk': order.id})
            return redirect('all-orders')
        
        
    context = {
        'form':form, 
        'order':order,
        'google_api_key':google_api_key, 
        
    }
    

    return render(request, 'admin_dashboard/Orders/editOrder.html', context)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def deleteOrder(request, pk):
    
    order = BookDelivery.objects.get(order_number=pk)
    item = order.order_number
    
    if request.method == "POST":
        order.delete()
        messages.success(request, 'Deleted successfully')
        return redirect('all-orders')
    
    context = {
        'item':item
    }
    
    return render(request, 'admin_dashboard/delete.html', context)


""" CONTACT """

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def allMessages(request):
    
    all_messages = Contact.objects.all()
    
    
    context = {
        'all_messages':all_messages
    }
    
    
    return render(request, 'admin_dashboard/contact/allMessages.html', context)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def viewMessages(request, pk):
    
    all_messages = Contact.objects.all()
    message = Contact.objects.get(id=pk)
    
    context = {
        'message':message,
        'all_messages': all_messages
    }
    
    return render(request, 'admin_dashboard/contact/viewMessage.html', context)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def deleteMessage(request, pk):
    
    message = Contact.objects.get(id=pk)
    item = message.name
    
    if request.method == "POST":
        message.delete()
        messages.success(request, 'Message Deleted!')
        return redirect('all-messages')
    
    context = {
        'item':item
    }
    
    
    return render(request, 'admin_dashboard/delete.html', context)


""" DELIVERY DETAILS """

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def viewDeliveryType(request):
    
    deliveryType = DeliveryType.objects.all()
    
    form = AddDeliveryTypeForm()
    
    if request.method == "POST":
        form = AddDeliveryTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added Successfully")
            return redirect('add-delivery-type')
        
    context = {
        'form':form, 
        'deliveryType':deliveryType
    }
    
    return render(request, 'admin_dashboard/delivery_details/deliveryType.html', context)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def editDeliveryType(request, pk):
    
    delivery_type = DeliveryType.objects.get(id=pk)
    
    form = AddDeliveryTypeForm(instance=delivery_type)
    
    if request.method == "POST":
        form = AddDeliveryTypeForm(request.POST, instance=delivery_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit Successfull')
            return redirect('add-delivery-type')
        
    context = {
        'form':form
    }
    
    return render(request, 'admin_dashboard/delivery_details/editDeliveryType.html', context)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def viewDeliveryAction(request):
    
    deliveryAction = DeliveryAction.objects.all()
    form = AddDeliveryActionForm()

    if request.method == "POST":
        form = AddDeliveryActionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added Successfully")
            return redirect('add-delivery-action')

    context = {
        'form': form, 
        'deliveryAction':deliveryAction
    }

    return render(request, 'admin_dashboard/delivery_details/deliveryAction.html', context)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def editDeliveryAction(request, pk):

    delivery_action = DeliveryAction.objects.get(id=pk)

    form = AddDeliveryActionForm(instance=delivery_action)

    if request.method == "POST":
        form = AddDeliveryActionForm(request.POST, instance=delivery_action)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit Successfull')
            return redirect('add-delivery-action')

    context = {
        'form': form
    }

    return render(request, 'admin_dashboard/delivery_details/editDeliveryAction.html', context)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def deleteDeliveryAction(request, pk):
    
    delivery_action = DeliveryAction.objects.get(id=pk)
    item = delivery_action.action
    
    if request.method == "POST":
        delivery_action.delete()
        messages.success(request, "delete successfull")
        return redirect('add-delivery-action')
    
    context = { 
        'delivery_action': delivery_action, 
        'item':item
    }
    
    
    return render(request, 'admin_dashboard/delete.html', context)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def deleteDeliveryType(request, pk):

    delivery_type = DeliveryType.objects.get(id=pk)
    item = delivery_type.item_type

    if request.method == "POST":
        delivery_type.delete()
        messages.success(request, "delete successfull")
        return redirect('add-delivery-type')

    context = {
        'delivery_type': delivery_type,
        'item': item
    }

    return render(request, 'admin_dashboard/delete.html', context)


""" DELIVERY PRICE """

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def addDeliveryMultiplier(request):
    
    record = DeliveryMultiplier.objects.all()
    
    if not record:
        messages.error(request, "Only one record allowed")
    
        if request.method == "POST":
            multiplier = request.POST.get('multiplier')
            add_multiplier = DeliveryMultiplier(multiplier=multiplier)
            add_multiplier.save()
            messages.success(request, 'Multuplier Added')
            return redirect('view-multiplier')
    
    return render(request, 'admin_dashboard/delivery_price/add.html')


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def viewDeliveryMultiplier(request):
    
    multipliers = DeliveryMultiplier.objects.all()
    
    #convert multiplier to string
    multiplier_strings = [
        str(multiplier.multiplier) for multiplier in multipliers
    ]
    
    
    context = {
        'multiplier_strings':multiplier_strings,
        'multipliers':multipliers
    }
    
    return render(request, 'admin_dashboard/delivery_price/view.html', context)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def editDeliveryMultiplier(request, pk):
    
    multiplier = DeliveryMultiplier.objects.get(id=pk)
    
    if request.method == "POST":
        new_multiplier = request.POST['multiplier']
        multiplier.multiplier = new_multiplier
        multiplier.save()
        messages.success(request, 'Multuplier Edited')
        return redirect('view-multiplier')
    
    
    context = {
        'multiplier':multiplier
    }
        
    
    return render(request, 'admin_dashboard/delivery_price/edit.html', context)
    
    
    


    
    
