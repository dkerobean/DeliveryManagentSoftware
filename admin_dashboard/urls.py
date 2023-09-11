from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.homePage, name="admin-home"),

    path('login/', views.loginPage, name="admin-login"),

    path('orders/', views.allOrders, name="all-orders"),
    path('order/add/', views.addOrder, name="add-order"),
    path('order/edit/<str:pk>/', views.editOrder, name="edit-order"),
    path('order/<str:pk>/', views.orderDetails, name="order-details"),
    path('order/delete/<str:pk>/', views.deleteOrder, name="delete-order"),

    path('messages/', views.allMessages, name="all-messages"),
    path('messages/<str:pk>/', views.viewMessages, name="view-message"),
    path('message/delete/<str:pk>/', views.deleteMessage, name="delete-message"), # noqa

    path('deliverytype/add/', views.viewDeliveryType, name="add-delivery-type"), # noqa
    path('deliverytype/edit/<str:pk>/', views.editDeliveryType, name="edit-delivery-type"), # noqa
    path('deliverytype/delete/<str:pk>/',views.deleteDeliveryType, name="delete-delivery-type"), # noqa

    path('deliveryaction/add/', views.viewDeliveryAction, name="add-delivery-action"), # noqa
    path('deliveryaction/edit/<str:pk>/',views.editDeliveryAction, name="edit-delivery-action"), # noqa
    path('deliveryaction/delete/<str:pk>/', views.deleteDeliveryAction, name="delete-delivery-action"), # noqa

    path('multiplier/add/', views.addDeliveryMultiplier, name="add-multiplier"), # noqa
    path('multiplier/view/', views.viewDeliveryMultiplier, name="view-multiplier"), # noqa
    path('multiplier/edit/<str:pk>/', views.editDeliveryMultiplier, name="edit-multiplier") # noqa

]
