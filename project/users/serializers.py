import logging
import re

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from rest_framework import serializers
from core.serializers import URIBaseModelSerializer
from users.models import Profile


logger = logging.getLogger('console-basic')
User = get_user_model()

# ------------------------------------------------------------------------------------------------
# -- Mixins --

class GetAuthUserSerializerMixin(serializers.Serializer):
    """Base for getting the auth user to the serializer"""
    def _get_user(self):
            request = self.context.get('request', None)
            if request:
                return request.user
            else:
                return None


class PasswordSerializerMixin(serializers.Serializer):

    new_password1 = serializers.CharField(
        label='New Password',
        required=True,
        error_messages={"blank": "This field must not be blank"}
    )
    new_password2 = serializers.CharField(
        label='Confirm new Password',
        write_only=True,
        required=True,
        error_messages={"blank": "This field must not be blank"}
    )

    def validate_new_password2(self, value):
        """Make sure both passwords match"""
        data = self.get_initial()
        new_password1 = data.get('new_password1')
        new_password2 = value
        if new_password1 != new_password2:
            raise serializers.ValidationError('Both passwords must match')
        return value

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user



# ------------------------------------------------------------------------------------------------
# -- User Serializers --


class UserSerializer(URIBaseModelSerializer):
    """Serializer for listing users"""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'is_verified',
            'is_private',
            'is_active',
            'uri',
        )
        read_only_fields = fields

    def _get_user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        else:
            return None


class UserDetailSerializer(serializers.ModelSerializer):
    """Retrieving a user Instance"""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'is_private',
            'is_active',
            'is_verified',
            'follow_user_uri',
        )
        read_only_fields = fields

    def _get_user(self):
        request = self.context.get('request', None)
        if request:
            return request.user


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer to create a User. The field 'password2' is ignored
    and only used for matching confirmation"""
    password2 = serializers.CharField(
        label='Confirm Password',
        write_only=True,
        )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            'password2',
        )
        extra_kwargs = {
            'password': {'write_only': True,
                         'min_length': 6,
                        },
        }
        read_only_fields = ('id',)

    def __init__(self, *args, **kwargs):
        super(CreateUserSerializer, self).__init__(*args, **kwargs)
        self.fields["username"].error_messages["blank"] = "This field is required"
        self.fields["email"].error_messages["blank"] = "This field is required"
        self.fields["password"].error_messages["blank"] = "This field is required"
        self.fields["password2"].error_messages["blank"] = "This field is required"
    
    def validate_email(self, value):        
        user = User.objects.filter(email=value).first()
        if user:
            if user.social_auth.exists():
                msg_social = 'Email is already in use with a social account'
                raise serializers.ValidationError(msg_social)
            else:
                msg_unique = 'User with this email already exists'
                raise serializers.ValidationError(msg_unique)

        return value

    def validate_password2(self, value):
        data = self.get_initial()
        password1 = data.get('password')
        if password1 != value:
            raise serializers.ValidationError('Both passwords must match')
        return value

    def validate_username(self, value):
        """Make sure no spaces are within the username. 
        Empty spaces at the start and end are stripped."""
        if " " in value:
            raise serializers.ValidationError('Empty spaces not allowed in username')
        if not re.match(r'^[A-Za-z0-9_]+$', value):
            raise serializers.ValidationError('Only upper-case and lower-case letters, numbers and underscores allowed')
        
        return value

    def create(self, validated_data):
        """Create a new user with an encrypted password and return it."""
        password2 = validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class SetPasswordSerializer(PasswordSerializerMixin):
    """Setting an auth user's password for when signed up with social-auth"""

    def validate(self, attrs):
        user = self.context['request'].user
        if user.has_usable_password():
            raise serializers.ValidationError('A previous password has been set already')
        return attrs


class UpdatePasswordSerializer(PasswordSerializerMixin):
    """Changing the user's password"""
    old_password = serializers.CharField(
        required=True,
        error_messages={"blank": "This field must not be blank"}
    )

    def validate_old_password(self, value):
        """If check fails, returns False"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Old password is incorrect. Please enter it again')
            )
        return value

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Login serializer for the user authentication object. Will return a auth token"""
    email = serializers.CharField(
        required=True,
        error_messages={"blank": "This field must not be blank"}
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        error_messages={"blank": "This field must not be blank"}
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if user:
            user.is_active = True
            user.save()
        else:
            msg = {"detail": 'Unable to login with that email and password combination'}
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """Used for reseting a user's password through the 'password reset' email."""
    new_password = serializers.CharField(
        label='New Password',
        required=True,
        error_messages={"blank": "This field must not be blank"}
    )
    new_password2 = serializers.CharField(
        label='Confirm New Password',
        write_only=True,
        required=True,
        error_messages={"blank": "This field must not be blank"}
    )

    def validate_new_password2(self, value):
        """Making sure both entered passwords match"""
        data = self.get_initial()
        new_password = data.get('new_password')
        new_password2 = value
        if new_password != new_password2:
            raise serializers.ValidationError('Both passwords must match')
        return value


class ProfileGetSerializer(serializers.ModelSerializer):
    """For retrieving the user's own Profile"""
    id = serializers.IntegerField(
        source='user.pk',
        read_only=True
    )
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    dob = serializers.DateField(
        allow_null=True,
        required=False
    )
    locale = serializers.CharField(read_only=True)
    is_private = serializers.BooleanField(source='user.is_private')
    is_verified = serializers.BooleanField(
        source='user.is_verified',
        read_only=True,
    )

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'dob',
            'is_verified',
            'locale',
            'is_private',
        )
        read_only_fields = (
            'id', 
            'is_verified',
            'locale',
            'dob',
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """For updating the user's own Profile"""
    id = serializers.IntegerField(
        source='user.pk',
        read_only=True
    )
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    locale = serializers.CharField(read_only=True)
    is_private = serializers.BooleanField(source='user.is_private')
    is_verified = serializers.BooleanField(
        source='user.is_verified',
        read_only=True,
    )

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_verified',
            'locale',
            'is_private',
        )
        read_only_fields = (
            'id', 
            'is_verified',
            'locale',
        )

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateSerializer, self).__init__(*args, **kwargs)
        self.fields["username"].error_messages["blank"] = "This field is required"
        self.fields["email"].error_messages["blank"] = "This field is required"
        self.fields["password"].error_messages["blank"] = "This field is required"
        self.fields["password2"].error_messages["blank"] = "This field is required"
    
    def validate_email(self, value):
        """Check if new email is already in use, excluding the current user's email.
        Could move to separate endpoint."""
        user = self._get_user()
        if User.objects.filter(email=value).exclude(email=user.email).exists():
            raise serializers.ValidationError('Email already in use')
        return value
    
    def validate_username(self, value):
        """Check if new username is already in use, excluding the current user's email.
        Could move to separate endpoint."""
        user = self._get_user()
        if User.objects.filter(username=value).exclude(username=user.username).exists():
            raise serializers.ValidationError('Username already in use')
        return value

    def update(self, instance, validated_data):        
        user_data = validated_data.pop('user', None)
        instance = super().update(instance, validated_data)

        if user_data:
            for (key, value) in user_data.items():
                setattr(instance.user, key, value)
            instance.user.save()  

        return instance

    def _get_user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        else:
            None