from django.shortcuts import render


def homePage(request):
    
    return render(request, 'admin_dashboard/index.html')


def loginPage(request):

    return render(request, 'admin_dashboard/Auth/login.html')
