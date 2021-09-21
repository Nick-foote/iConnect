import logging

from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token
from users.models import Profile


logger = logging.getLogger(__name__)

# ---- USERS ----

# TODO 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def new_user_setup(sender, instance=None, created=False, **kwargs):
    """Makes an auth token when a User is created and sends """
    if created:
        Profile.objects.create(user=instance) 

        try:
            Token.objects.create(user=instance)
        except ValueError:
            logger.exception(f"Error creating AuthToken for user id: {instance}")
        