from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter

from users import views

app_name = 'users'

# router = DefaultRouter()

urlpatterns = [

    path('accounts/login/',
         views.SpotifyLoginView.as_view(),
         name='temp',
         ),

    path('users/me/',
         views.ProfileView.as_view(),
         name='profile',
         ),

    path('test/login/',
         views.TESTSpotifyLoginView.as_view(),
         name='wiplogin',
         ),

    path('my-redirect/',
         views.SpotifyLoginView.as_view(),
         name='wiplogin',
         ),

    path('spotify-auth/',
         views.SpotifyAuthView.as_view(),
         name='wiplogin',
         ),
]