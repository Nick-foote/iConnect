from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from playlists.views import PlaylistViewSet


router = DefaultRouter()

router.register(prefix='api/v1/playlists', viewset=PlaylistViewSet, basename='playlist')

urlpatterns = [
    path('', include(router.urls)),
]