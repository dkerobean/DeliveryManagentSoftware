from django.urls import path
from . import views 


urlpatterns = [
    path('dashboard/', views.homePage, name="user_home"), 
    path('orders/', views.ordersPage, name="user_order"), 
    path('profile/', views.editProfile, name="edit-profile"),
]
