from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="user-login")
def homePage(request):
    
    return render(request, 'user_dashboard/index.html')
