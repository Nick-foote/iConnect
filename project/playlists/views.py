from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import GeometryDistance, Distance
from django.contrib.gis.measure import D

from rest_framework import viewsets

from playlists.models import Playlist
from playlists.serializers import PlaylistGetSerializer, PlaylistCreateSerializer
from playlists.spotify_manager import SpotifyManager

# TODO: add pagination. Zooming out gets next

class PlaylistViewSet(viewsets.ModelViewSet):
    """Returns only playlists listened to in the last three months.
    Excludes private data."""    

    def __init__(self, **kwargs: Any) -> None:
        self.user_location = self.get_user_location()
        super().__init__(**kwargs)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return PlaylistGetSerializer
        elif self.action == 'create':
            return PlaylistCreateSerializer

    def get_queryset(self):
        """
        Only returns the closest 20 playlists to the current user, 
        with a spatial limit of 25miles.
        """
        # TODO: exclude current auth user's playlists so a user doesn't see their own activity
        
        if not self.user_location:
            queryset = Playlist.public.all()
        else:
            queryset = Playlist.public.filter(
                location__distance_lte=(self.user_location, D(mi=25))
                )
            
            #     .order_by(GeometryDistance("location", user_location))
            #     # could annoatate distance for later use
            queryset = queryset[:20]  

        return queryset

    def retrieve(self, request, *args, **kwargs):
        self.connect_to_spotify()
        return super().retrieve(request, *args, **kwargs)

    def get_user_location(self):
        """Retrieve user coordinates from the frontend and converts the param to two floats"""
        user_coords = self.request.GET.get("latlong", None)
        if not user_coords:
            self.user_latlong = None
        lat, long = [float(x) for x in user_coords.split(",")[:2]]
        # requires swappping coords around for PostGIS
        return Point(long, lat, srid=4326)

    def connect_to_spotify(self):
        """Confirms the username is associated to a Spotify Account and then uploads"""
        sp = SpotifyManager(self.request.user)
        user_on_spotify = sp.user_query()
        if not user_on_spotify:
            return

        sp.upload_playlist(location=self.user_location)
