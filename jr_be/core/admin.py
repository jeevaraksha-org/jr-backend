"""
/** ARMS product**/
/***********************************************************************************************************
* This software has been developed free of cost and intended for public usage.                             *
* Copyright © 2020 Archit Jha, Rajath S Bharadwaj, Mohit Rajesh Chugh, Samaresh Panda. All Rights Reserved.*
* For more information write to arms4product@gmail.com.                                                    *
************************************************************************************************************
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['phone', 'name']
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        (
            'Permissions',
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (
            'Important dates',
            {'fields': ('last_login',)}
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.TestServiceModel)
admin.site.register(models.OTPModel)
admin.site.register(models.JR_USER)
admin.site.register(models.JR_USER_HEALTH_HIST)
admin.site.register(models.JR_VOLUNTEER)
admin.site.register(models.JR_SERVICE_USER)
admin.site.register(models.JR_SERVICE_VOLUNTEER)
admin.site.register(models.JR_SERVICE_VOLUNTEER_ACPT_RJCT)
admin.site.register(models.JR_VOLUNTEER_DND)
admin.site.register(models.VOLUNTEER_LOC)
admin.site.register(models.JR_CASE)
admin.site.register(models.JR_SERVICE_STATUS)
admin.site.register(models.FCMDevices)
admin.site.register(models.DocumentUpload)

