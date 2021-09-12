# from django.db import models
from django.contrib.gis.db import models as models
# from django.utils.translation import gettext_lazy as _

from django.conf import settings
# class TimeStampedModelGIS

class Activity(models.Model):
    """Activity/interaction"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='playlist',
        )
    playlist = models.ForeignKey(
        "Playlist", 
        on_delete=models.CASCADE
        )
    location = models.PointField(srid=4326)
    # area = models.models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return "my string"
    # def __str__(self) -> str:
    #     return f"{self.user.username} Playlist {self.playlist.name} Activity"

class Playlist(models.Model):
    """Individual item on Spotify"""
    name = models.CharField(
        max_length=250, 
        null=True,
        default="un-named",
        )
    uri = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name} - {self.uri}"
