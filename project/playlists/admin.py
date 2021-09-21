from django.contrib import admin
from django.utils.translation import gettext as _
from leaflet.admin import LeafletGeoAdmin
from playlists.models import Playlist

# ------------------------------------------------------------------------------------------------
#   --   Models    --


@admin.register(Playlist)
class PlaylistAdmin(LeafletGeoAdmin):
    ordering = ['id']
    list_display = ['id', 'name']
    search_fields = ['user', 'name']
    list_per_page = 50

    fieldsets = (
        (_("Info"), {'fields': (
            'user', 
            'name', 
            'spotify_uri', 
            'location', 
            'created_at', 
            'updated_at', 
            'is_private', 
            )}), 
            )
    readonly_fields = ['created_at', 'updated_at']
