from django.db import models
import uuid


class DeliveryMultiplier(models.Model):
    multiplier = models.FloatField()
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def save(self, *args, **kwargs):
        if self.pk:
            raise ValueError("Only One Record Allowed")
        super().save(*args, **kwargs)
       
    
    def __str__(self):
        return self.multiplier
    



