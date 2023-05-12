from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.homePage, name="home"), 
    
    path('login/', views.userLogin, name="user-login"),
    path('register/', views.userSignUp, name="user-register"),
    path('logout/', views.userLogout, name="user-logout"),
    
    path('book-delivery/', views.bookDelivery, name="book-delivery"), 
    path('confirm_delivery/', views.confirmDelivery, name="confirm-delivery"), 
    
    path('contact/', views.contactPage, name="contact"), 
    
    path('track-order/', views.trackOrder, name="track-order"),
    path('order-results/', views.orderResults, name="order-results"),
    
    
    
]

