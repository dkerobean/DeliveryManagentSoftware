from django.urls import path
from . import views 


urlpatterns = [
    path('dashboard/', views.homePage, name="user_home"), 
    
    path('orders/<str:pk>/', views.ordersPage, name="user_order"),
    path('order/<str:pk>/', views.deleteOrder, name="delete-user-order"),
    
    
    path('profile/<str:pk>/', views.editProfile, name="edit-profile"),
    
]
