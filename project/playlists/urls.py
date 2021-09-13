from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter

from playlists.views import ActivityViewSet, PlaylistViewSet

router = DefaultRouter()

router.register(prefix='api/v1/', viewset=ActivityViewSet, basename='activity')
router.register(prefix='api/v1/', viewset=PlaylistViewSet, basename='playlist')
