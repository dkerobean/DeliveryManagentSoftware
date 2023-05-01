from django.shortcuts import render


def homePage(request):
    
    return render(request, 'admin_dasboard/index.html')
