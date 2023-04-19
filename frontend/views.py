from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm


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
