from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('registration-send-otp/', views.RegSendOTPView.as_view(), name='send-otp-register'),
    path('registration-receive-otp/', views.RegReceiveOTPView.as_view(), name='receive-otp-register'),
    path('register-user/', views.RegisterUserView.as_view(), name='register-user'),
    path('update-user/', views.UpdateUserView.as_view(), name='update-user'),
    path('medhist-user/', views.HealthHistView.as_view(), name='medhist-user'),
    path('login-send-otp/', views.LoginSendOTPView.as_view(), name='send-otp-login'),
    path('login-receive-otp/', views.LoginReceiveOTPView.as_view(), name='receive-otp-login'),
    path('user-profile/', views.UserInfoView.as_view(), name='user-profile'),
]
