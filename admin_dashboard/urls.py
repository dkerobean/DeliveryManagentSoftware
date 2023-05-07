from django.urls import path
from . import views 


urlpatterns = [
    path('home/', views.homePage, name="admin-home"), 
    
    path('login/', views.loginPage, name="admin-login"), 
    
    path('orders/', views.allOrders, name="all-orders"), 
    path('order/add/', views.addOrder, name="add-order"),
    path('order/edit/<str:pk>/', views.editOrder, name="edit-order"),
    path('order/<str:pk>/', views.orderDetails, name="order-details"), 
    
    path('messages/', views.allMessages, name="all-messages"),
    path('messages/<str:pk>/', views.viewMessages, name="view-message"),
    
    path('deliverytype/add/', views.viewDeliveryType, name="add-delivery-type"),
    path('deliveryaction/add/', views.viewDeliveryAction, name="add-delivery-action"),
    
    
]