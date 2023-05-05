from django.urls import path
from . import views 


urlpatterns = [
    path('home/', views.homePage, name="admin-home"), 
    
    path('login/', views.loginPage, name="admin-login"), 
    
    path('orders/', views.allOrders, name="all-orders"), 
    path('order/add/', views.addOrder, name="add-order"),
    path('order/<str:pk>/', views.orderDetails, name="order-details"), 
    
]