"""
/** ARMS product**/
/***********************************************************************************************************
* This software has been developed free of cost and intended for public usage.                             *
* Copyright © 2020 Archit Jha, Rajath S Bharadwaj, Mohit Rajesh Chugh, Samaresh Panda. All Rights Reserved.*
* For more information write to arms4product@gmail.com.                                                    *
************************************************************************************************************
"""
import random
from django.utils import timezone
import json
import datetime
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework.permissions import IsAuthenticated
import googlemaps
from pyfcm import FCMNotification
from .serializers import ServiceUserDetailSerializer
from core.models import User, JR_USER, JR_VOLUNTEER, VOLUNTEER_LOC, JR_VOLUNTEER_DND, \
                        JR_SERVICE_USER,JR_SERVICE_VOLUNTEER,JR_SERVICE_VOLUNTEER_ACPT_RJCT, \
                        JR_CASE, JR_SERVICE_STATUS, FCMDevices


def distance_mat(u_lat, u_long, v_lat, v_long):
    gmaps = googlemaps.Client(key='REDACTED')

    origins = {"lat": v_long, "lng": v_lat}
    print(origins)
    destinations = {"lat": u_lat, "lng": u_long}
    print(destinations)

    distance_matrx = gmaps.distance_matrix(origins, destinations)
    return distance_matrx


def send_push(push_token, service_id):
    push_service = FCMNotification(
        api_key="REDACTED")

    registration_id = str(push_token)
    message_title = "Service Id:" + str(service_id)
    message_body = "Your help is required for medical emergency."
    result = push_service.notify_single_device(registration_id=registration_id,
                                               message_title=message_title, message_body=message_body)
    print(result)


class CreateRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        unique_id = False
        user_phone = request.user.phone
        json_data = json.loads(request.body)
        if json_data:
            service_desc = json_data["servicedesc"]
            service_req_for = json_data["servicereqfor"]
            user_latitude = json_data["latitude"]
            user_longitude = json_data["longitude"]
            user_loc = Point(user_longitude, user_latitude)
            service_dt_tm = datetime.datetime.now()

            while not unique_id:
                service_id = random.randint(9999, 9999999)
                query = JR_SERVICE_USER.objects.filter(SERVICE_ID=service_id)
                if query:
                    unique_id = False
                else:
                    unique_id = True

            user_model = User.objects.get(phone=user_phone)

            data_service_user = JR_SERVICE_USER(
                SERVICE_ID=service_id, USER_PH_NO=user_model,
                SERVICE_DESC=service_desc, SERVICE_REQ_FOR=service_req_for,
                SERVICE_USER_LOC=user_loc, SERVICE_DATE_TIME=service_dt_tm,
                SERVICE_STATUS=True

            )
            data_service_user.save()
            v_queryset = VOLUNTEER_LOC.objects.annotate(distance=Distance('VOLUNTEER_CURR_LOC', user_loc)).order_by(
                'distance')[0:10]

            service_model = JR_SERVICE_USER.objects.get(SERVICE_ID=service_id)

            for volunteer in v_queryset:
                v_user_model = User.objects.get(phone=volunteer.VOLUNTEER_PH_NO)
                data_v_request = JR_SERVICE_VOLUNTEER_ACPT_RJCT(
                    SERVICE_ID=service_model, VOLUNTEER_PH_NO=v_user_model,

                )
                data_v_request.save()
 
                fcm_model = FCMDevices.objects.get(USER_PH_NO=v_user_model)
                push_token = fcm_model.DEVICE_TOKEN
                send_push(push_token, service_id)



            data_status_request = JR_SERVICE_STATUS(
                SERVICE_ID=service_model, IS_ACTIVE=True
            )

            data_status_request.save()

            return Response({
                'status': 'success',
                'message': 'Service Created',
                'service_id': service_id
            })

        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })


class VolunteerAcptRjctView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_phone = request.user.phone
        json_data = json.loads(request.body)
        if json_data:
            service_id = json_data["serviceid"]
            service_flag = json_data["serviceflag"]
            print(service_flag)
            user_model = User.objects.get(phone=user_phone)
            service_model = JR_SERVICE_USER.objects.get(SERVICE_ID=service_id)
            curr_model = JR_SERVICE_VOLUNTEER_ACPT_RJCT.objects.filter(SERVICE_ID__SERVICE_ID=service_id)
            status_model = JR_SERVICE_STATUS.objects.get(SERVICE_ID__SERVICE_ID=service_id)
            if service_model.SERVICE_STATUS:
                if service_flag == "Accept":
                    for query in curr_model:
                        if query.VOLUNTEER_PH_NO == user_model:
                            query.IS_ACCEPT = True
                            query.save()
                            service_model.SERVICE_STATUS = False
                            service_model.save()
                            status_model.STATUS = "IN-PROGRESS"
                            status_model.save()
                            return Response({
                                'status': 'success',
                                'message': 'Request Accepted'
                            })

                else:
                    for query in curr_model:
                        if query.VOLUNTEER_PH_NO == user_model:
                            query.IS_REJECT = True
                            query.save()
                            service_model.SERVICE_FLAG = False
                            return Response({
                                'status': 'success',
                                'message': 'Request Rejected'
                            })
            else:
                return Response({
                    'status': 'failure',
                    'message': 'Request already assigned or closed'
                })


class VolunteerDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_phone = request.user.phone
        response_flag = False
        json_data = json.loads(request.body)
        if json_data:
            service_id = json_data["serviceid"]
            service_model = JR_SERVICE_USER.objects.get(SERVICE_ID=service_id)
            queryset = JR_SERVICE_VOLUNTEER_ACPT_RJCT.objects.filter(SERVICE_ID__SERVICE_ID=service_id)
            for volunteer in queryset:
                if volunteer.IS_ACCEPT:
                    v_phone = volunteer.VOLUNTEER_PH_NO
                    user_model = User.objects.get(phone=v_phone)
                    v_name = user_model.name
                    loc_model = VOLUNTEER_LOC.objects.get(VOLUNTEER_PH_NO=v_phone)
                    v_loc = loc_model.VOLUNTEER_CURR_LOC
                    loc_list = [coord for coord in v_loc]
                    v_longitude = loc_list[0]
                    v_latitude = loc_list[1]
                    content = {
                        'status': 'success',
                        'phone': user_model.phone,
                        'name': user_model.name,
                        'longitude': v_longitude,
                        'latitude': v_latitude
                    }
                    response_flag = True
                    break
            if response_flag:
                json.dumps(content)
                return Response(content)
            else:
                return Response({
                    'status': 'failure',
                    'message': 'Not Accepted by Volunteer Yet'
                })
        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })


class ServiceUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        json_data = json.loads(request.body)
        if json_data:
            service_id = json_data["service_id"]

            queryset = JR_SERVICE_USER.objects.get(SERVICE_ID=service_id)
            service_model = JR_SERVICE_USER.objects.get(SERVICE_ID=service_id)
            user_loc = service_model.SERVICE_USER_LOC
            user_model = User.objects.get(phone=service_model.USER_PH_NO)
            loc_list = [coord for coord in user_loc]
            u_longitude = loc_list[0]
            u_latitude = loc_list[1]
            return Response({
                "status": "success",
                "service_id": service_model.SERVICE_ID,
                "case_desc": service_model.SERVICE_DESC,
                "user_ph_no": user_model.phone,
                "longitude": u_longitude,
                "latitude": u_latitude

            })
        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'

            })



class VolunteerLocationTrackerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_phone = request.user.phone
        json_data = json.loads(request.body)
        if json_data:
            volun_phone = json_data["phone"]

            queryset = VOLUNTEER_LOC.objects.get(VOLUNTEER_PH_NO__phone=volun_phone)
            v_loc = queryset.VOLUNTEER_CURR_LOC
            loc_list = [coord for coord in v_loc]
            v_longitude = loc_list[0]
            v_latitude = loc_list[1]

            return Response({
                'status': 'success',
                'longitude': v_longitude,
                'latitude': v_latitude

            })
        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'

            })


class DistanceMatrix(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        if json_data:
            service_id = json_data["serviceid"]
            service_model = JR_SERVICE_USER.objects.get(SERVICE_ID=service_id)
            u_loc = service_model.SERVICE_USER_LOC
            loc_list = [coord for coord in u_loc]
            u_longitude = loc_list[0]
            u_latitude = loc_list[1]
            queryset = JR_SERVICE_VOLUNTEER_ACPT_RJCT.objects.filter(SERVICE_ID__SERVICE_ID=service_id)
            for volunteer in queryset:
                if volunteer.IS_ACCEPT:
                    v_phone = volunteer.VOLUNTEER_PH_NO
                    user_model = User.objects.get(phone=v_phone)
                    loc_model = VOLUNTEER_LOC.objects.get(VOLUNTEER_PH_NO=v_phone)
                    v_loc = loc_model.VOLUNTEER_CURR_LOC
                    loc_list = [coord for coord in v_loc]
                    v_longitude = loc_list[1]
                    v_latitude = loc_list[0]
                    dist_mat = distance_mat(u_latitude, u_longitude, v_latitude, v_longitude)

                    content = {'status': 'success', 'distance_matrix': dist_mat}
                    json.dumps(content)
            return Response(content)
        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })


class CaseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        volun_phone = request.user.phone
        json_data = json.loads(request.body)
        if json_data:
            case_desc = json_data["casedesc"]
            service_id = json_data["serviceid"]

            vouln_model = User.objects.get(phone=volun_phone)
            service_model = JR_SERVICE_USER.objects.get(SERVICE_ID=service_id)
            user_phone = service_model.USER_PH_NO
            user_model = User.objects.get(phone=user_phone)

            data = JR_CASE(
                CASE_DESC=case_desc, SERVICE_ID=service_model,
                USER_PH_NO=user_model, VOLUNTEER_PH_NO=vouln_model
            )

            data.save()

            service_model.SERVICE_STATUS = False
            service_model.save()

            return Response({
                'status': 'success',
                'message': 'Case details submitted'
            })

        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })


class CancelService(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_phone = request.user.phone
        json_data = json.loads(request.body)
        if json_data:
            service_id = json_data["serviceid"]
            service_status = json_data["service_status"]
            print(service_status)
            reason = json_data["reason"]
            user_model = User.objects.get(phone=user_phone)
            service_model = JR_SERVICE_STATUS.objects.get(SERVICE_ID__SERVICE_ID=service_id)
            usr_service_model = JR_SERVICE_USER.objects.get(SERVICE_ID=service_id)
            vol_acp_rj_model = JR_SERVICE_VOLUNTEER_ACPT_RJCT.objects.filter(SERVICE_ID__SERVICE_ID=service_id)
            if service_status == "volunteer":
                service_model.CANCELLED_BY_VOLUNTEER = True
                service_model.STATUS = "CANCELLED"
                usr_service_model.SERVICE_STATUS = True
                for query in vol_acp_rj_model:
                    if query.VOLUNTEER_PH_NO == user_model:
                        query.IS_REJECT = True
                        query.IS_ACCEPT = False
                        query.save()
            if service_status == "user":
                service_model.CANCELLED_BY_USER = True
                service_model.STATUS = "CANCELLED"
            if service_status == "reached":
                service_model.IS_ACTIVE = False
                print(service_status)
            if reason:
                service_model.REASON = reason

            service_model.save()
            usr_service_model.save()
            return Response({
                'status': 'success',
                'message': 'Service Status Changed'
            })
        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })


class GetFCMToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        phone = request.user.phone
        current_user_model = User.objects.get(phone=phone)
        json_data = json.loads(request.body)
        if json_data:
            fcm_token = json_data["fcm_token"]

            user_fcm_model = FCMDevices.objects.get(USER_PH_NO__phone=phone)
            user_fcm_model.DEVICE_TOKEN = fcm_token
            user_fcm_model.save()

            print(fcm_token)

            return Response({
                'status': 'success',
                'message': 'Received Token'
            })

        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })


class GetServiceDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_phone = request.user.phone
        content = {}
        case = []
        count = 1
        no_count = 0
        current_user_model = User.objects.get(phone=user_phone)
        volunteer_info = JR_SERVICE_VOLUNTEER_ACPT_RJCT.objects.filter(VOLUNTEER_PH_NO=current_user_model)
        for volunteer in volunteer_info:
            if volunteer.SERVICE_ID:
                service_id = volunteer.SERVICE_ID
                usr_service_model = JR_SERVICE_USER.objects.get(SERVICE_ID=service_id.SERVICE_ID)
                datetime_now = timezone.now()
                service_dt = usr_service_model.SERVICE_DATE_TIME 
                service_exp = service_dt + datetime.timedelta(minutes=15)
                service_is_expired = False
                if datetime_now > service_exp:
                    service_is_expired = True
                service_status_model = JR_SERVICE_STATUS.objects.get(SERVICE_ID=service_id)
                if not service_status_model.CANCELLED_BY_USER and not volunteer.IS_REJECT and not service_is_expired and usr_service_model.SERVICE_STATUS:
                    service_model = JR_SERVICE_USER.objects.get(SERVICE_ID=service_id.SERVICE_ID)
                    print(service_model)
                    user_loc = service_model.SERVICE_USER_LOC
                    print(user_loc)
                    user_model = User.objects.get(phone=service_model.USER_PH_NO)
                    loc_list = [coord for coord in user_loc]
                    u_longitude = loc_list[0]
                    u_latitude = loc_list[1]
                    case_itr = {
                        "service_id": service_model.SERVICE_ID,
                        "case_desc": service_model.SERVICE_DESC,
                        "user_ph_no": user_model.phone,
                        "user_name": user_model.name,
                        "longitude": u_longitude,
                        "latitude": u_latitude
                    }
                    case.append(case_itr)
                   # content.update({str(count): case_itr})
                    count += 1
        content.update({'Cases': case})
        json.dumps(content)
        return Response(content)


class RequestCancelledStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_phone = request.user.phone
        json_data = json.loads(request.body)
        if json_data:
            service_id = json_data["serviceid"]
            print(service_id)
            service_status_model = JR_SERVICE_STATUS.objects.get(SERVICE_ID__SERVICE_ID=service_id)
            if service_status_model.CANCELLED_BY_USER:
                message = "Request cancelled by User"
            elif service_status_model.CANCELLED_BY_VOLUNTEER:
                message = "Request cancelled by Volunteer"
            elif not service_status_model.IS_ACTIVE:
                message = "Reached"
            else:
                message = "Request is in active state"
            return Response({
                'status': 'success',
                'message': message
            })
        else:
            return Response({
                'status': 'failure',
                'message': 'No data received'
            })
