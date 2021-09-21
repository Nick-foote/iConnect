from datetime import date, timedelta
from django.contrib.gis.db import models as models

from django.conf import settings


# ------------------------------------------------------------------------------------------------
# -- MANAGERS --

class RecentPublicManger(models.Manager):
    """ Returns only public activity with the last three months."""

    def get_queryset(self):
        today = date.today()
        three_mnths_ago = today - timedelta(3 * 30)
        
        return super().get_queryset().filter(
            is_private=False,
            created_at__gte=three_mnths_ago,
            ) \
            


# ------------------------------------------------------------------------------------------------
# -- MODELS --

class TimeStampedModelGIS(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract= True


class Playlist(TimeStampedModelGIS):
    """Activity/interaction"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='playlist',
        )
    name = models.CharField(
        max_length=250, 
        null=True,
        default="un-named",
        )
    spotify_uri = models.CharField(max_length=250)
    location = models.PointField(srid=4326, geography=True)
    is_private =models.BooleanField(default=False)

    public = RecentPublicManger()

    def __str__(self) -> str:
        return f"{self.user.username} Playlist {self.name} Activity"

    @property
    def get_readable_date(self):
        """Formatting the datetime to date"""
        return self.created_at.strftime("%a %d-%b-%Y")
