from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from frontend.models import Profile, BookDelivery
from django.contrib.auth.models import User
from django.contrib import messages


@login_required(login_url="user-login")
def homePage(request):
    
    user = request.user.profile
    deliveries = user.deliveries.all()
    
    context = {
        'deliveries':deliveries,
        'user':user
    }     
    return render(request, 'user_dashboard/index.html', context)


@login_required(login_url="user-login")
def editProfile(request, pk):
    
    user = Profile.objects.get(id=pk)
    form = ProfileForm(instance=user)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated')
            return redirect('user_home')
    
    
    context = {
        'form':form, 
        'user':user
    }
    
    
    return render(request, 'user_dashboard/edit_profile.html', context)


@login_required(login_url="user-login")
def ordersPage(request, pk):
    
    user = Profile.objects.get(id=pk)
    deliveries = user.deliveries.filter(is_deleted=False)
    completed = user.deliveries.filter(order_status="Completed")
    pending = user.deliveries.filter(order_status="Pending")
    cancelled = user.deliveries.filter(is_deleted="True")
    
    context = {
        'deliveries':deliveries,
        'completed':completed, 
        'pending':pending, 
        'cancelled':cancelled, 
        'user':user
    }
    
    
    return render(request, 'user_dashboard/orders.html', context)


@login_required(login_url="user-login")
def deleteOrder(request, pk):

    order = BookDelivery.objects.get(order_number=pk)
    item = order.order_number

    if request.method == "POST":
        order.delete()
        messages.success(request, 'Deleted successfully')
        return redirect('user_order')

    context = {
        'item': item
    }

    return render(request, 'user_dashboard/delete.html', context)
