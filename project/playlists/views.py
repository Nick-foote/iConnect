from django.shortcuts import render
from rest_framework import viewsets

from playlists.models import Playlist, Activity
from playlists.serializers import ActivitySerializer, PlaylistSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """tbc"""

    # add prefetch_related, exclude private
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    """tbc"""

    # add prefetch_related, exclude private
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer