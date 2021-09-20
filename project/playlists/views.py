# from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import GeometryDistance

from rest_framework import viewsets

from playlists.models import Playlist
from playlists.serializers import PlaylistGetSerializer, PlaylistCreateSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    """Returns only playlists listened to in the last three months.
    Excludes private data."""    

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return PlaylistGetSerializer
        elif self.action == 'create':
            return PlaylistCreateSerializer

    def get_queryset(self):
        """
        Only returns the closest 20 playlists to the current user, 
        with a spatial limit of 10kms.
        """
        # TODO: exclude current auth user's playlists so a user doesn't see their own activity
        user_location = self.get_user_location()
        if not user_location:
            queryset = Playlist.public.all()
        else:
            queryset = Playlist.public.filter(location__dwithin=(user_location, 10000)) \
                .order_by(GeometryDistance("location", user_location))
                # could annoatate distance for later use
            queryset = queryset[:20]  

        return queryset

    def perform_save(self, serializer):
        user_location = self.get_user_location()
        serializer.save(user_location)
    
    def get_user_location(self):
        """"""
        # Get user coords
        user_coords = self.request.GET.get("coord", None)
        if not user_coords:
            return
        long, lat = user_coords.split(",")[:2]
        return Point(long, lat, srid=4326)

