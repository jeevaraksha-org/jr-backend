"""
/** ARMS product**/
/***********************************************************************************************************
* This software has been developed free of cost and intended for public usage.                             *
* Copyright © 2020 Archit Jha, Rajath S Bharadwaj, Mohit Rajesh Chugh, Samaresh Panda. All Rights Reserved.*
* For more information write to arms4product@gmail.com.                                                    *
************************************************************************************************************
"""
from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        """Creates and saves a new user"""
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password):
        """Creates and saves a new super-user"""
        user = self.create_user(phone, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using phone instead of username"""
    phone = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'


class JR_USER(models.Model):
    """Custom user model for Application Users"""
    USER_PH_NO = models.ForeignKey(User, on_delete=models.CASCADE)
    USER_FIRST_NM = models.CharField(max_length=100)
    USER_MIDDLE_NM = models.CharField(max_length=100, blank=True)
    USER_LAST_NM = models.CharField(max_length=100, blank=True)
    USER_EMAIL = models.EmailField(max_length=100, blank=True)
    USER_EMERGENCY_NO = models.CharField(max_length=12, blank=True)
    USER_GENDER = models.CharField(max_length=1)
    USER_DOB = models.DateField(max_length=8)
    USER_BLOOD_GROUP = models.CharField(max_length=10)
    USER_ADDR1 = models.CharField(max_length=255, blank=True)
    USER_ADDR2 = models.CharField(max_length=255, blank=True)
    USER_CITY = models.CharField(max_length=255, blank=True)
    USER_STATE = models.CharField(max_length=255, blank=True)
    USER_COUNTRY = models.CharField(max_length=255, blank=True)
    USER_PINCODE = models.CharField(max_length=255, blank=True)
    USER_IS_VOLUNTEER = models.BooleanField(default=False)
    D_CREATION_DT = models.DateTimeField(auto_now_add=True)
    D_UPDATE_DT = models.DateTimeField(auto_now_add=True)




class JR_USER_HEALTH_HIST(models.Model):
    """Custom user HEALTH HISTORY model for Application USER"""
    USER_PH_NO = models.ForeignKey(User, on_delete=models.CASCADE)
    USER_HH_CONDITION_NM = models.CharField(max_length=255, blank=True)
    USER_HH_ALLERGY_DESC = models.CharField(max_length=255, blank=True)
    USER_HH_MED_ALLERGY_DESC = models.CharField(max_length=255, blank=True)




class JR_VOLUNTEER(models.Model):
    """Custom Volunteer model"""
    VOLUNTEER_PH_NO = models.ForeignKey(User, on_delete=models.CASCADE)
    VOLUNTEER_LEVEL_ID = models.CharField(max_length=22)
    VOLUNTEER_NAME = models.CharField(max_length=100)
    VOLUNTEER_TITLE = models.CharField(max_length=100)
    VOLUNTEER_EMAIL = models.CharField(max_length=100)
    VOLUNTEER_GENDER = models.CharField(max_length=1)
    VOLUNTEER_DOB = models.DateField(max_length=8)
    VOLUNTEER_ADDR = models.CharField(max_length=255, blank=True)
    VOLUNTEER_CITY = models.CharField(max_length=255, blank=True)
    VOLUNTEER_STATE = models.CharField(max_length=255, blank=True)
    VOLUNTEER_COUNTRY = models.CharField(max_length=255, blank=True)
    VOLUNTEER_PINCODE = models.CharField(max_length=255, blank=True)
    VOLUNTEER_SPECIALITY = models.CharField(max_length=100, blank=True)
    VOLUNTEER_IS_CERTIFIED = models.BooleanField(default=False)
    D_CREATION_DT = models.DateTimeField(auto_now_add=True)
    D_UPDATE_DT = models.DateTimeField(auto_now_add=True)




class VOLUNTEER_LOC(models.Model):
    VOLUNTEER_PH_NO = models.ForeignKey(User, on_delete=models.CASCADE)
    VOLUNTEER_CURR_LOC = models.PointField(blank=True)




class JR_VOLUNTEER_DND(models.Model):
    """DND Model for Volunteers to opt in or out of services"""
    VOLUNTEER_PH_NO = models.ForeignKey(User, on_delete=models.CASCADE)
    DND_FL = models.BooleanField(default=False)




class JR_SERVICE_USER(models.Model):
    SERVICE_ID = models.IntegerField(blank=False)
    USER_PH_NO = models.ForeignKey(User, on_delete=models.CASCADE)
    SERVICE_DESC = models.CharField(max_length=255)
    SERVICE_REQ_FOR = models.CharField(max_length=10)
    SERVICE_USER_LOC = models.PointField(blank=True)
    SERVICE_DATE_TIME = models.DateTimeField(auto_now_add=True)
    SERVICE_STATUS = models.BooleanField(default=False)


class JR_SERVICE_VOLUNTEER(models.Model):
    SERVICE_ID = models.ForeignKey(JR_SERVICE_USER, on_delete=models.CASCADE)
    VOLUNTEER_PH_NO = models.ForeignKey(User, on_delete=models.CASCADE)
    SERVICE_DESC = models.CharField(max_length=255)
    SERVICE_REQ_FOR = models.CharField(max_length=10)
    SERVICE_VOLUNTEER_LOC = models.PointField(blank=True)
    SERVICE_DATE_TIME = models.DateTimeField(auto_now_add=True)




class JR_SERVICE_VOLUNTEER_ACPT_RJCT(models.Model):
    SERVICE_ID = models.ForeignKey(JR_SERVICE_USER, on_delete=models.CASCADE)
    VOLUNTEER_PH_NO = models.ForeignKey(User, on_delete=models.CASCADE)
    IS_ACCEPT = models.BooleanField(default=False)
    IS_REJECT = models.BooleanField(default=False)



class JR_CASE(models.Model):
    CASE_DESC = models.CharField(max_length=255, blank=True)
    SERVICE_ID = models.ForeignKey(JR_SERVICE_USER, on_delete=models.CASCADE)
    USER_PH_NO = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_phone')
    VOLUNTEER_PH_NO = models.ForeignKey(User, on_delete=models.CASCADE, related_name='volunteer_phone')
    CASE_DT_TM = models.DateTimeField(auto_now_add=True)


class JR_SERVICE_STATUS(models.Model):
    SERVICE_ID = models.ForeignKey(JR_SERVICE_USER, on_delete=models.CASCADE)
    IS_ACTIVE = models.BooleanField(default=False)
    CANCELLED_BY_USER = models.BooleanField(default=False)
    CANCELLED_BY_VOLUNTEER = models.BooleanField(default=False)
    STATUS = models.CharField(max_length=20, blank=True)
    REASON = models.CharField(max_length=255, blank=True)



class OTPModel(models.Model):
    """OTP model for OTP verification of users"""
    phone = models.CharField(max_length=12, unique=True)
    otp = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)


class TestServiceModel(models.Model):
    """Model to test Volunteer view"""
    phone = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)


class DocumentUpload(models.Model):
    description = models.CharField(max_length=200)
    document = models.FileField()
    upload_time_stamp = models.DateTimeField(auto_now_add=True)


class FCMDevices(models.Model):
    USER_PH_NO = models.ForeignKey(User, on_delete=models.CASCADE)
    DEVICE_TOKEN = models.CharField(max_length=255, blank=True)



