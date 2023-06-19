from django.db import models


class DeliveryMultiplier(models.Model):
    multiplier = models.FloatField()
    
    def __str__(self):
        return self.multiplier
    



