"""
/** ARMS product**/
/***********************************************************************************************************
* This software has been developed free of cost and intended for public usage.                             *
* Copyright © 2020 Archit Jha, Rajath S Bharadwaj, Mohit Rajesh Chugh, Samaresh Panda. All Rights Reserved.*
* For more information write to arms4product@gmail.com.                                                    *
************************************************************************************************************
"""

import random
import json
import http.client
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from rest_framework.parsers import JSONParser
from rest_framework import generics
from .serializers import UserSerializer, AuthTokenSerializer, UserProfileSerializer, \
                            UserHealthHistorySerializer
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from drf_multiple_model.views import FlatMultipleModelAPIView
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from core.models import User, JR_USER, JR_USER_HEALTH_HIST,\
                        OTPModel, TestServiceModel, FCMDevices
from datetime import datetime

def send_otp(phone, otp):

    conn = http.client.HTTPConnection("2factor.in")

    payload = ""

    headers = {'content-type': "application/x-www-form-urlencoded"}

    otp_request = "/API/V1/7f6098e5-dc03-11ea-9fa5-0200cd936042/SMS/" + str(phone) + "/" + str(otp) + "/UserRegistration"


    conn.request("GET", otp_request, payload,
                 headers)

    res = conn.getresponse()
    data = res.read()
    print(data)


class CreateUserView(generics.CreateAPIView):
    # Create a new user in the system
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    #Create a new auth token for user
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class RegSendOTPView(APIView):

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        if json_data:
            phone_number = json_data["phone"]
            otp = random.randint(999, 9999)
            queryset1 = User.objects.filter(phone=phone_number)
            queryset2 = OTPModel.objects.filter(phone=phone_number)
            if queryset1:
                return Response({
                    'status': 'failure',
                    'message': 'User already exists, Try logging in'
                })
            elif queryset2:
                data_info = queryset2[0]
                data_info.otp = otp
                data_info.is_verified = False
                data_info.save()
                send_otp(phone_number, otp)
                return Response({
                    'status': 'success',
                    'message': 'OTP Sent'
                })
            else:
                data_info = OTPModel(phone=phone_number, otp=otp)
                data_info.save()
                return Response({
                    'status': 'success',
                    'message': 'OTP Sent'
                })
        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })


class RegReceiveOTPView(APIView):

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        if json_data:
            user_phone = json_data["phone"]
            user_otp = json_data["otp"]
            queryset = OTPModel.objects.get(phone=user_phone)
            if queryset.otp == user_otp:
                queryset.is_verified = True
                queryset.save()
                return Response({
                    'status': 'success',
                    'message': 'OTP Verified'
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


class RegisterUserView(APIView):

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        if json_data:
            phone = json_data["phone"]
            firstname = json_data["firstname"]
            middlename = json_data["middlename"]
            lastname = json_data["lastname"]
            gender = json_data["gender"]
            emergency_contact = json_data["emergencycontact"]
            dob = json_data["dateofbirth"]
            dob = dob[:10]
            blood_group = json_data["bloodgroup"]

            password = str(phone) + "hello"

            queryset_core = User.objects.filter(phone=phone)
            query_is_verified = OTPModel.objects.filter(phone=phone)

            if queryset_core:
                return Response({
                    'status': 'failure',
                    'message': 'User already exists, Try logging in'
                })

            else:

                if query_is_verified:
                    queryset = query_is_verified[0]

                    if queryset.is_verified:
                        get_user_model().objects.create_user(phone, password)
                        current_user_model = User.objects.get(phone=phone)
                        current_user_model.name = firstname
                        current_user_model.save()

                        user_personal_info = JR_USER(
                            USER_PH_NO=current_user_model, USER_FIRST_NM=firstname, USER_MIDDLE_NM=middlename,
                            USER_LAST_NM=lastname, USER_GENDER=gender, USER_BLOOD_GROUP=blood_group,
                            USER_DOB=dob, USER_EMERGENCY_NO=emergency_contact
                        )

                        user_personal_info.save()

                        user_health_history = JR_USER_HEALTH_HIST(
                            USER_PH_NO=current_user_model
                        )

                        user_health_history.save()

                        user_fcm_info = FCMDevices(
                            USER_PH_NO=current_user_model,
                        )

                        user_fcm_info.save()

                        token = Token.objects.create(user=current_user_model)

                        return Response(
                            {
                                'status': 'success',
                                'message': 'User registration success',
                                'auth_token': 'token ' +token.key
                            }
                        )
                    else:
                        return Response(
                            {
                                'status': 'failure',
                                'message': 'Phone number not verified'
                            }
                        )
                else:
                    return Response({
                        'status': 'failure',
                        'message': 'Phone number not verified'
                    })
        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_phone = request.user.phone
        json_data = json.loads(request.body)
        if json_data:
            firstname = json_data["firstname"]
            middlename = json_data["middlename"]
            lastname = json_data["lastname"]
            gender = json_data["gender"]
            emergency_contact = json_data["emergencycontact"]
            dob = json_data["dateofbirth"]
            dob = dob[:10]
            blood_group = json_data["bloodgroup"]
            email = json_data["email"]
            addr1 = json_data["addr1"]
            addr2 = json_data["addr2"]
            city = json_data["city"]
            state = json_data["state"]
            country = json_data["country"]
            pincode = json_data["pincode"]

            current_user_model = JR_USER.objects.get(USER_PH_NO__phone=user_phone)
            current_user_model.USER_FIRST_NM = firstname
            current_user_model.USER_MIDDLE_NM = middlename
            current_user_model.USER_LAST_NM = lastname
            current_user_model.USER_EMAIL = email
            current_user_model.USER_EMERGENCY_NO = emergency_contact
            current_user_model.USER_GENDER = gender
            current_user_model.USER_DOB = dob
            current_user_model.USER_BLOOD_GROUP = blood_group
            current_user_model.USER_ADDR1 = addr1
            current_user_model.USER_ADDR2 = addr2
            current_user_model.USER_CITY = city
            current_user_model.USER_STATE = state
            current_user_model.USER_COUNTRY = country
            current_user_model.USER_PINCODE = pincode

            current_user_model.save()

            return Response({
                'status': 'success',
                'message': 'Profile updated successfully'
            })

        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })


class HealthHistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_phone = request.user.phone
        json_data = json.loads(request.body)
        health_con = " "
        if json_data:
            allergies = json_data["allergies"]
            med_allergies = json_data["allmed"]
            current_user_model = JR_USER_HEALTH_HIST.objects.get(USER_PH_NO__phone=user_phone)
            hh_list = []
            for health_condition in json_data:
                if json_data[health_condition] == True :
                    hh_list.append(health_condition)
            for i in hh_list:
                health_con += i + ", "

            current_user_model.USER_HH_CONDITION_NM = health_con
            current_user_model.USER_HH_ALLERGY_DESC = allergies
            current_user_model.USER_HH_MED_ALLERGY_DESC = med_allergies
            current_user_model.save()

            return Response({
                'status': 'success',
                'message': 'Health History Successfuly Updated'
            })
        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })


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


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_phone = request.user.phone
        health_dict = {}
        health_list = []
        health_comp_list = []
        queryset = JR_USER.objects.get(USER_PH_NO__phone=user_phone)
        serializer_class = UserProfileSerializer(queryset)
        user_profile_data = serializer_class.data
        queryset = JR_USER_HEALTH_HIST.objects.get(USER_PH_NO__phone=user_phone)
        serializer_class = UserHealthHistorySerializer(queryset)
        user_health_history = serializer_class.data

        queryset = JR_USER_HEALTH_HIST.objects.get(USER_PH_NO__phone=user_phone)
        hh = queryset.USER_HH_CONDITION_NM
        hh = hh.split(',')
        hh.pop()
        for i in hh:
            i = i.strip()
            health_dict.update({str(i): True})
            health_list.append({str(i): True})
        health_dict.update({ "allergies": queryset.USER_HH_ALLERGY_DESC })
        health_list.append({ "allergies": queryset.USER_HH_ALLERGY_DESC })
        health_dict.update({ "allmed": queryset.USER_HH_MED_ALLERGY_DESC })
        health_list.append({ "allmed": queryset.USER_HH_MED_ALLERGY_DESC })
        health_comp_list.append(health_dict)
        content = {'status':'success', 'UserInfo': user_profile_data, 'HealthHistory': health_comp_list}
        json.dumps(content)
        return Response(content)

