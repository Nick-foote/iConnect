from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter

from users import views

app_name = 'users'

urlpatterns = [
    path('accounts/login/',
         views.SpotifyLoginView.as_view(),
         name='sp-login',
         ),
]