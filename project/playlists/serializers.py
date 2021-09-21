# from datetime import datetime
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from playlists.models import Playlist



class PlaylistGetSerializer(GeoFeatureModelSerializer):
    """Creating a Playlist"""
    user = serializers.CharField(source='user.username')
    date_listened = serializers.SerializerMethodField(source='user.get_readable_date')
    distance_to_user = serializers.SerializerMethodField()

    class Meta:

        model = Playlist
        fields = [
            'user',
            'name',
            'spotify_uri',
            'location',
            'date_listened',
            'distance_to_user',
            'updated_at',
            ]
        geo_field = 'location'
        read_only_fields = fields

    def get_date_listened(self, obj):
        return obj.get_readable_date

    def get_distance_to_user(self, obj):
        """Calculating how far away the user was to the current auth user when the
        playlist was listened to."""
        pass


class PlaylistCreateSerializer(serializers.Serializer):
    """Creating a Playlist only, recording time the user listened to."""

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
                
    
    def save(self, user_location=None):
        user = self._get_user()
        if all(user_location, user):
            Playlist.objects.create(
                user=user,
                location=user_location,
                # name=
                # spotify_uri=
            )
        pass

    def _get_user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        else:
            return None

    def _get_recent_spotify_playlist(self):
        """"""
        pass

