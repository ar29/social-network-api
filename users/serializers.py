from rest_framework import serializers
from .models import CustomUser, FriendRequest
from django.contrib.auth.hashers import make_password
# users/serializers.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                raise serializers.ValidationError(_('No active account found with the given credentials'))
        else:
            raise serializers.ValidationError(_('Must include "email" and "password".'))

        refresh = self.get_token(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'email': user.email,
                'id': user.id
            }
        }

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser

        fields = ['id', 'email', 'password']


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        # Adding the below line made it work for me.
        instance.is_active = True
        if password is not None:
            # Set password does the hash, so you don't need to call make_password 
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)
    

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'is_accepted', 'timestamp']
