from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from frontend.models import BookDelivery
from .forms import EditDeliveryForm, BookDeliveryForm
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


    
    
