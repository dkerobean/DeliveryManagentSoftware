from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from frontend.models import Profile
from django.contrib.auth.models import User
from django.contrib import messages


@login_required(login_url="user-login")
def homePage(request):
    
    user = request.user.profile
    deliveries = user.deliveries.all()
    
    context = {
        'deliveries':deliveries
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
    deliveries = user.deliveries.all()
    
    context = {
        'deliveries':deliveries       
    }
    
    
    return render(request, 'user_dashboard/orders.html', context)
