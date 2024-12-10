from django.urls import path
from volunteer import views

app_name = 'volunteer'

urlpatterns = [
    path('login-send-otp/', views.LoginSendOTPView.as_view(), name='send-otp'),
    path('login-receive-otp/', views.LoginReceiveOTPView.as_view(), name='receive-otp'),
    path('update-volunteer/', views.UpdateVolunteerView.as_view(), name='update-volunteer'),
    path('volunteer-dnd/', views.DndStatusView.as_view(), name='volunteer-dnd'),
    path('volunteer-loc/', views.VolunteerLocationView.as_view(), name='volunteer-loc'),
    path('volunteer-profile/', views.VolunteerProfileView.as_view(), name='volunteer-profile'),

]
