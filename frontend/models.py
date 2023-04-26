from django.db import models
import uuid 
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True,
                                      upload_to='profiles', default='profiles/user-default.png')
    
    
    def __str__(self):
        return self.name
    
    
class BookDelivery(models.Model):
    item = models.CharField(max_length=200, blank=True, null=True)
    item_type = models.CharField(max_length=200, blank=True, null=True)
    pickup_location = models.CharField(max_length=250, blank=True, null=True)
    destination_location = models.CharField(max_length=250, blank=True, null=True)
    sender_contact = models.CharField(max_length=200, blank=True, null=True)
    reciever_contact = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.item
    
    
    
    
    


