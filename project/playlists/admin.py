from django.contrib import admin
from django.utils.translation import gettext as _
from leaflet.admin import LeafletGeoAdmin
from playlists.models import Activity, Playlist

# ------------------------------------------------------------------------------------------------
#   --   Models    --


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name']
    search_fields = ['name']
    list_per_page = 50

    fieldsets = (
        (_("Info"), {'fields': (
            'name', 
            'uri', 
            )}),            
     )
    # readonly_fields = ()


@admin.register(Activity)
class ActivityAdmin(LeafletGeoAdmin):
    ordering = ['id']
    list_display = ['id', 'user', 'playlist', 'location']
    search_fields = ['name']
    list_per_page = 50

    fieldsets = (
        (_("Info"), {'fields': (
            'user', 
            'playlist', 
            'location', 
            'created_at', 
            'updated_at', 
            )}), 
            )
    readonly_fields = ['created_at', 'updated_at']

