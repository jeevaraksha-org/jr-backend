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
from core.models import JR_VOLUNTEER, VOLUNTEER_LOC, JR_VOLUNTEER_DND


class VolunteerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = JR_VOLUNTEER
        fields = '__all__'


class VolunteerLocSerializer(serializers.ModelSerializer):

    class Meta:
        model = VOLUNTEER_LOC
        fields = '__all__'


class VolunteerDNDSerializer(serializers.ModelSerializer):

    class Meta:
        model = JR_VOLUNTEER_DND
        fields = '__all__'
