from django.shortcuts import render


""" HOME PAGE """
def homePage(request):    
    
    return render(request, 'frontend/index.html')


""" USER AUTH PAGES """

def userLogin(request):    
    
    return render(request, 'frontend/login.html')


def userSignUp(request):
    
    return render(request, 'frontend/register.html')


""" 404 PAGE """

def handler404(request, exception):
    
    return render(request, 'frontend/404.html', status=404)
