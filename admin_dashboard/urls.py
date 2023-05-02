from django.urls import path
from . import views 


urlpatterns = [
    path('home/', views.homePage, name="admin-home"), 
    path('login/', views.loginPage, name="admin-login")
]