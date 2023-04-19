from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.homePage, name="home"), 
    
    path('login/', views.userLogin, name="user-login"),
    path('register/', views.userSignUp, name="user-register"),
    path('logout/', views.userLogout, name="user-logout"), 
    
    
]

