"""
/** ARMS product**/
/***********************************************************************************************************
* This software has been developed free of cost and intended for public usage.                             *
* Copyright © 2020 Archit Jha, Rajath S Bharadwaj, Mohit Rajesh Chugh, Samaresh Panda. All Rights Reserved.*
* For more information write to arms4product@gmail.com.                                                    *
************************************************************************************************************
"""

from django.urls import path
from services import views

app_name = 'services'

urlpatterns = [
    path('create-request/', views.CreateRequestView.as_view(), name='create_request'),
    path('volunteer-approval/', views.VolunteerAcptRjctView.as_view(), name='volunteer-approval'),
    path('volunteer-details/', views.VolunteerDetailsView.as_view(), name='volunteer-details'),
    path('volunteer-loc-tracker/', views.VolunteerLocationTrackerView.as_view(), name='volunteer-loc-tracker'),
    path('distance-matrix/', views.DistanceMatrix.as_view(), name='distance-matrix'),
    path('create-case/', views.CaseCreateView.as_view(), name='create-case'),
    path('cancel-service/', views.CancelService.as_view(), name='cancel-service'),
    path('service-details/', views.GetServiceDetailsView.as_view(), name='service-details'),
    path('service-status/', views.RequestCancelledStatusView.as_view(), name='service-status'),
    path('get-token/', views.GetFCMToken.as_view(), name='get-fcm-token'),

]
