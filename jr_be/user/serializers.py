"""
/** ARMS product**/
/***********************************************************************************************************
* This software has been developed free of cost and intended for public usage.                             *
* Copyright © 2020 Archit Jha, Rajath S Bharadwaj, Mohit Rajesh Chugh, Samaresh Panda. All Rights Reserved.*
* For more information write to arms4product@gmail.com.                                                    *
************************************************************************************************************
"""

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from core.models import TestServiceModel, User, JR_USER, JR_USER_HEALTH_HIST


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('phone', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for authentication object"""
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        phone = attrs.get('phone')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('requets'),
            username=phone,
            password=password

        )
        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = JR_USER
        fields = '__all__'


class UserHealthHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JR_USER_HEALTH_HIST
        fields = '__all__'
"""
class ListServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestServiceModel
        fields = ('id', 'phone', 'name', 'title', 'description')


class UserProfileSerializer(serializers.Serializer):

    class Meta:
        model = JR_USER
        fields = ('id', 'phone', 'first_name', 'middle_name', 'last_name',
                  'emergency_contact', 'gender', 'dob', 'blood_group')
"""
