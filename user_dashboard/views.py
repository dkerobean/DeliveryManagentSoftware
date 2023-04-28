from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="user-login")
def homePage(request):
    
    return render(request, 'user_dashboard/index.html')


@login_required(login_url="user-login")
def editProfile(request):
    
    
    return render(request, 'user_dashboard/edit_profile.html')


@login_required(login_url="user-login")
def ordersPage(request):
    
    return render(request, 'user_dashboard/orders.html')
