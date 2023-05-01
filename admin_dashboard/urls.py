from django.urls import path
from . import views 


urlpatterns = [
    path('index/', views.homePage, name="admin-home"), 
]