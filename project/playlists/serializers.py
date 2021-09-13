from django.db import models
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from playlists.models import Playlist, Activity


class ActivitySerializer(GeoFeatureModelSerializer):
    """tbc"""

    class Meta:

        model = Activity
        fields = [
            'user',
            'playlist',
            'location',
            'created_at',
            'updated_at',
            ]
        geo_field = 'location'
        # read_only_fields = []


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