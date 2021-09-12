import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import render
from rest_framework import authentication, generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings
from users.models import Profile
from users.serializers import (
    AuthTokenSerializer, CreateUserSerializer, SetPasswordSerializer, 
    UpdatePasswordSerializer, ProfileGetSerializer, ProfileUpdateSerializer
    )


User = get_user_model()
logger = logging.getLogger(name='console-basic')


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the db"""
    serializer_class = CreateUserSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        """Returns the AuthToken when creating a new user"""
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        response = super().create(request, *args, **kwargs)
        email = response.data["email"]
        username = response.data["username"]
        user_id = response.data["id"]

        # Precaution with create: Token should already have been created via signal
        token, created = Token.objects.get_or_create(user__id=user_id)

        new_user_data = {
            'id': user_id,
            'email': email,
            'username': username,
            'token': token.key
        }
        return Response(new_user_data, status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        """Activates user on login if previously deactivated"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.is_active = True
        user_logged_in.send(
            sender=user.__class__,
            request=request,
            user=user
        )
        token, created = Token.objects.get_or_create(user=user)
        response = {
            'user': user.id,
            'token': token.key,
        }
        return Response(response)


# ------------------------------------------------------------------------------------------------
# -- PASSWORDS --

class SetPasswordView(generics.UpdateAPIView):
    """Setting an auth user's password fow when signed up with social-auth"""
    serializer_class = SetPasswordSerializer
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password has been set successfully'
                    }
        return Response(response)


class UpdatePasswordView(generics.UpdateAPIView):
    """Update User's password. Old password confirmation required"""
    serializer_class = UpdatePasswordSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password has been updated successfully'
                    }
        return Response(response)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user: Retrieve & Update actions only."""

    def get_serializer_class(self):        
        return ProfileGetSerializer
        # if self.request.method == 'GET':
        #     return ProfileGetSerializer
        # elif self.request.method in ['PATCH', 'PUT']:
        #     return ProfileUpdateSerializer

    def get_object(self):
        """Retrieve and return authenticated user's profile."""
        return Profile.objects \
            .select_related("user") \
            .get(id=self.request.user.profile.pk)



# ------
# socialauth


class SpotifyLoginView(generics.GenericAPIView):
    """tbc"""
    authentication_classes = []
    permission_classes = []
    serializer_class = ProfileGetSerializer

    def get(self, request, *args, **kwargs):

        print(f"\n request: {request}\n")
        print(f"\n args: {args}\n")
        print(f"\n kwargs: {kwargs}\n")
        

        # form = PasswordResetForm()
        return render(
            request, 
            'accounts/login/login.html', 
            # {'form': form}
            )

class TESTSpotifyLoginView(generics.GenericAPIView):
    """tbc"""
    authentication_classes = []
    permission_classes = []
    serializer_class = ProfileGetSerializer

    def get(self, request, *args, **kwargs):

        print(f"\n request: {request}\n")
        print(f"\n args: {args}\n")
        print(f"\n kwargs: {kwargs}\n")
        

        # form = PasswordResetForm()
        return render(
            request, 
            'accounts/social-auth/spotify_login.html', 
            # {'form': form}
            )

class SpotifyAuthView(generics.GenericAPIView):
    """tbc"""
    authentication_classes = []
    permission_classes = []
    serializer_class = ProfileGetSerializer

    def get(self, request, *args, **kwargs):

        print(f"\n request: {request}\n")
        print(f"\n args: {args}\n")
        print(f"\n kwargs: {kwargs}\n")
        

        # form = PasswordResetForm()
        return render(
            request, 
            'accounts/social-auth/spotify_auth.html', 
            # {'form': form}
            )
