from django.db import models
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from playlists.models import Playlist, Activity


class PlaylistSerializer(serializers.ModelSerializer):
    """tbc"""

    class Meta:

        model = Playlist
        fields = [
            'name',
            'uri',
            'created_at',
            'updated_at',
            ]


class ActivitySerializer(GeoFeatureModelSerializer):
    """tbc"""
    user = serializers.CharField(source='user.username')
    playlist_name = serializers.CharField(source='playlist.name')
    playlist_uri = serializers.CharField(source='playlist.uri')

    class Meta:

        model = Activity
        fields = [
            'user',
            'playlist_name',
            'playlist_uri',
            'location',
            'created_at',
            'updated_at',
            ]
        geo_field = 'location'
        # read_only_fields = []

