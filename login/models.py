from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

#Create a new token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_type_wrapper(sender, instance=None, created=False, **kwargs):
    if created:
        try: 
            instance.usertypewrapper.is_lecturer
        except Exception as e:
            UserTypeWrapper.objects.create(user=instance, is_lecturer=False)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_email(sender, instance=None, created=False, **kwargs):
    if created:
        instance.email = instance.username + "@nottingham.ac.uk"
        instance.save()

#Class to hold extra information about a user
class UserTypeWrapper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_lecturer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
