from django.contrib import admin
from .models import Profile, BookDelivery, Contact, Rider, DeliveryType, DeliveryAction

admin.site.register(Profile)
admin.site.register(BookDelivery)
admin.site.register(Contact)
admin.site.register(Rider)
admin.site.register(DeliveryAction)
admin.site.register(DeliveryType)


