from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from frontend.models import BookDelivery, Contact, DeliveryAction, DeliveryType
from .forms import EditDeliveryForm, BookDeliveryForm, AddDeliveryActionForm, AddDeliveryTypeForm
import uuid 
from django.urls import reverse



# ceck if user has admin status
def is_admin(user):
    return user.is_authenticated and user.is_staff

""" HOME """
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def homePage(request):
    
    return render(request, 'admin_dashboard/index.html')


""" AUTENTHICATION """

def loginPage(request):
    
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin-home')
    
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.ogjects.get(username=username)
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
    
    orders = BookDelivery.objects.all()
    
    # add order 
    form = BookDeliveryForm()
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Order created successfully')
            return redirect('all-orders')
        
    context = {
        'orders':orders, 
        'form':form
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
    
    order = BookDelivery.objects.get(id=pk)
    form = EditDeliveryForm(instance=order)
    
    if request.method == "POST":
        form = EditDeliveryForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order edited successfully")
            url = reverse('order-details', kwargs={'pk': order.id})
            return redirect(url)
        
        
    context = {
        'form':form, 
        'order':order,
    }
    

    return render(request, 'admin_dashboard/Orders/editOrder.html', context)


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


    
    
