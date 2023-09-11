from django.db import models
import uuid


class DeliveryMultiplier(models.Model):
    multiplier = models.FloatField()
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
       
    
    def __str__(self):
        return self.multiplier
    



