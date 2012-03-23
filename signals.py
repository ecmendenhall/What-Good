from registration.signals import user_registered
from django.db.models import signals
from django.db.models.signals import post_save
from goodthings.models import UserProfile
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse

def createUserProfile(sender, instance, **kwargs):
    """Create a UserProfile object each time a User is created ; and link it.
    """
    UserProfile.objects.get_or_create(user=instance, defaults={'birthdate': '1901-01-01', 'sex': 'Male', })

signals.post_save.connect(createUserProfile, sender=User)


