from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from core.models import JR_SERVICE_USER


class ServiceUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = JR_SERVICE_USER
        fields = '__all__'

