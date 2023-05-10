from django.db import models
import uuid 
from django.contrib.auth.models import User
import random
import string
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True,
                                      upload_to='profiles', default='profiles/avatar.svg')
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    
    def __str__(self):
        return self.name
    
class Rider(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                            primary_key=True, editable=False)

    def __str__(self):
        return self.name
    
    
class BookDelivery(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='deliveries', null=True, blank=True)
    rider = models.ForeignKey(
        Rider, on_delete=models.CASCADE, related_name='rider', null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    item = models.CharField(max_length=200, blank=True, null=True)
    item_type = models.CharField(max_length=200, blank=True, null=True)
    pickup_location = models.CharField(max_length=250, blank=True, null=True)
    destination_location = models.CharField(max_length=250, blank=True, null=True)
    sender_contact = models.CharField(max_length=200, blank=True, null=True)
    reciever_contact = models.CharField(max_length=200, blank=True, null=True)
    order_number = models.CharField(max_length=10, unique=True, editable=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Soft delete 
    is_deleted = models.BooleanField(default=False)
    
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
    
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Assigned', 'Assigned'), 
        ('In-progress', 'In-progress'),
        ('Completed', 'Completed')
    ]
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    
    def save(self, *args, **kwargs):
        # Generate an order number if one doesn't already exist
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        # Get the current date as a string in the format "YYYYMMDD"
        date_string = datetime.now().strftime("%Y%m%d")

        # Get a random alphanumeric string of length 5
        random_string = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=5))

        # Combine the date string and random string to form the order number
        order_number = date_string + random_string

        return order_number

    
    def __str__(self):
        return self.item
    

class Contact(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    topic = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    
    def __str__(self):
        return self.name
    
class DeliveryType(models.Model):
    item_type = models.CharField(max_length=250, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return self.action
    
class DeliveryAction(models.Model):
    action = models.CharField(max_length=250, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return self.action
    
    
    
    

    
    
    
    
    
    
    
    
    


