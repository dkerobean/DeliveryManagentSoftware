from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):

    if created:
        user = instance
        profile = Profile.objects.create(  # noqa
            user=user,
            name=user.first_name,
            username=user.first_name,
            email=user.email,
            location=''
        )


@receiver(post_save, sender=Profile)
def updateProfile(sender, created, instance, **kwargs):

    profile = instance
    user = profile.user

    if not created:
        user.first_name = profile.name
        user.email = profile.email
        user.save()


@receiver(post_delete, sender=Profile)
def deleteProfile(sender, instance, **kwargs):
    user = instance.user
    user.delete()
