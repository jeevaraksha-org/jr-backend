"""
/** ARMS product**/
/***********************************************************************************************************
* This software has been developed free of cost and intended for public usage.                             *
* Copyright © 2020 Archit Jha, Rajath S Bharadwaj, Mohit Rajesh Chugh, Samaresh Panda. All Rights Reserved.*
* For more information write to arms4product@gmail.com.                                                    *
************************************************************************************************************
"""

import random
import http.client
import json
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from drf_multiple_model.views import FlatMultipleModelAPIView
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import VolunteerProfileSerializer, VolunteerLocSerializer, VolunteerDNDSerializer
from core.models import User, OTPModel, JR_VOLUNTEER, VOLUNTEER_LOC, JR_VOLUNTEER_DND

def send_otp(phone, otp):

    conn = http.client.HTTPConnection("2factor.in")

    payload = ""

    headers = {'content-type': "application/x-www-form-urlencoded"}

    otp_request = "/API/V1/7f6098e5-dc03-11ea-9fa5-0200cd936042/SMS/" + str(phone) + "/" + str(otp) + "/UserRegistration"

    # https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}/{template_name}

    conn.request("GET", otp_request, payload,
                 headers)

    res = conn.getresponse()
    data = res.read()

class LoginSendOTPView(APIView):

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        if json_data:
            phone_number = json_data["phone"]
            queryset = User.objects.filter(phone=phone_number)
            if not queryset:
                return Response({
                    'status': 'failure',
                    'message': 'User does not exists, Please register the user'
                })
            else:
                otp = random.randint(999, 9999)
                data_query = OTPModel.objects.get(phone=phone_number)
                data_query.otp = otp
                data_query.is_verified = False
                data_query.save()
                send_otp(phone_number, otp)
                return Response({
                    'status': 'success',
                    'message': 'OTP Sent'
                })
        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })


class LoginReceiveOTPView(APIView):

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        if json_data:
            user_phone = json_data["phone"]
            user_otp = json_data["otp"]
            queryset = OTPModel.objects.get(phone=user_phone)
            if queryset.otp == user_otp:
                queryset.is_verified = True
                queryset.save()
                user = User.objects.get(phone=user_phone)
                token = Token.objects.get(user=user)
                return Response({
                    'status': 'success',
                    'message': 'OTP Verified',
                    'auth_token': 'token ' + token.key
                })
            else:
                return Response({
                    'status': 'failure',
                    'message': 'OTP Verification Failed'
                })
        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })


class UpdateVolunteerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_phone = request.user.phone
        json_data = json.loads(request.body)
        if json_data:
            addr = json_data["addr"]
            city = json_data["city"]
            state = json_data["state"]
            country = json_data["country"]
            pincode = json_data["pincode"]

        current_user_model = JR_VOLUNTEER.objects.get(VOLUNTEER_PH_NO__phone=user_phone)
        current_user_model.VOLUNTEER_ADDR = addr
        current_user_model.VOLUNTEER_CITY = city
        current_user_model.VOLUNTEER_STATE = state
        current_user_model.VOLUNTEER_COUNTRY = country
        current_user_model.VOLUNTEER_PINCODE = pincode

        current_user_model.save()

        return Response({
            'status': 'success',
            'message': 'Profile updated successfully'
        })


class DndStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_phone = request.user.phone
        json_data = json.loads(request.body)
        if json_data:
            dnd_status = json_data["dndstatus"]
            current_user_model = JR_VOLUNTEER_DND.objects.get(VOLUNTEER_PH_NO__phone=user_phone)
            if dnd_status == True:
                current_user_model.DND_FL = True
            else:
                current_user_model.DND_FL = False

            current_user_model.save()
            msg = 'User DND Status set to ' + str(current_user_model.DND_FL)
            return Response({
                'status': 'success',
                'message': msg
            })
        else:
            return Response({
                'status': 'failure',
                'message': 'No Data Received'
            })


class VolunteerLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_phone = request.user.phone
        json_data = json.loads(request.body)
        if json_data:
            latitude = json_data["latitude"]
            print(latitude)
            longitude = json_data["longitude"]
            print(longitude)
            current_user_model = VOLUNTEER_LOC.objects.get(VOLUNTEER_PH_NO__phone=user_phone)
            current_user_model.VOLUNTEER_CURR_LOC = Point(longitude, latitude)
            current_user_model.save()

            print(current_user_model.VOLUNTEER_CURR_LOC)

            return Response({
                'status': 'success',
                'message': 'Location Updated'
            })


        else:
            return Response({
                'status': 'failure',
                'message': 'No Data Received'
            })


class VolunteerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_phone = request.user.phone
        queryset_volunteer = JR_VOLUNTEER.objects.get(VOLUNTEER_PH_NO__phone=user_phone)
        serializer_volunteer = VolunteerProfileSerializer(queryset_volunteer)
        volunteer_data = serializer_volunteer.data
        queryset_dnd = JR_VOLUNTEER_DND.objects.get(VOLUNTEER_PH_NO__phone=user_phone)
        serializer_dnd = VolunteerDNDSerializer(queryset_dnd)
        dnd_data = serializer_dnd.data
        queryset_loc = VOLUNTEER_LOC.objects.get(VOLUNTEER_PH_NO__phone=user_phone)
        serializer_loc = VolunteerLocSerializer(queryset_loc)
        loc_data = serializer_loc.data
        content = {'status': 'success',
                   'VolunteerInfo': volunteer_data,
                   'DNDStatus': dnd_data,
                   'Location': loc_data
                   }
        json.dumps(content)
        return Response(content)

