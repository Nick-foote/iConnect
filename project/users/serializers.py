import logging
import re

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework import serializers


logger = logging.getLogger(__name__)
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
            'password': {'write_only': True, 'min_length': 8,},
        }
        read_only_fields = ('id',)

        
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
