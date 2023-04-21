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
    
    
    


