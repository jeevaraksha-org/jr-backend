"""
/** ARMS product**/
/***********************************************************************************************************
* This software has been developed free of cost and intended for public usage.                             *
* Copyright © 2020 Archit Jha, Rajath S Bharadwaj, Mohit Rajesh Chugh, Samaresh Panda. All Rights Reserved.*
* For more information write to arms4product@gmail.com.                                                    *
************************************************************************************************************
"""

import os
import csv
from django.shortcuts import render
from django.contrib.gis.geos import Point
from .forms import Upload_Form
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from core.models import User, JR_USER, JR_VOLUNTEER, VOLUNTEER_LOC, JR_VOLUNTEER_DND, \
                        JR_SERVICE_USER,JR_SERVICE_VOLUNTEER,JR_SERVICE_VOLUNTEER_ACPT_RJCT, \
                        JR_CASE, OTPModel, FCMDevices


#path = os.path.dirname(os.path.dirname(os.path.abspath("media"))) + "jr_be/file_upload/media/"


def upload_excel_csv(request):
    form = Upload_Form()
    if request.method == 'POST':
        form = Upload_Form(request.POST, request.FILES)
        if form.is_valid():
            upload_dat = form.save(commit=False)
            upload_dat.document = request.FILES['document']
            print(upload_dat.document)
            file_type = upload_dat.document.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type != 'csv':
                return render(request, 'file_upload/error.html')
            upload_dat.save()
           # print(os.path.exists(path))
            file_path = "/home/admin/jr-app/jr_be/file_upload/media/" + str(upload_dat.document)
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    data_row = row
                    name = data_row[0]
                    title = data_row[1]
                    level = data_row[2]
                    phone = data_row[3]
                    email = data_row[4]
                    dob = data_row[5]
                    dob = dob.split("/")
                    try:
                        date_birth = dob[2] + "-" + dob[1] + "-" + dob[0]
                    except IndexError:
                        date_birth = "2000-01-01"
                    gender = data_row[6]
                    certified = data_row[7]
                    if certified == 'yes' or certified == 'Yes':
                        is_certified = True
                    else:
                        is_certified = False

                    password = str(phone) + "hello"

                    check_model = User.objects.filter(phone=phone)
                    if check_model:
                        print("User with phone number: " + phone + " already exists")

                    else:

                        get_user_model().objects.create_user(phone, password)
                        current_user_model = User.objects.get(phone=phone)
                        current_user_model.name = name
                        current_user_model.save()

                        user_personal_info = JR_USER(
                            USER_PH_NO=current_user_model, USER_FIRST_NM=name, USER_GENDER=gender,
                            USER_DOB=date_birth, USER_EMAIL=email
                        )
                        user_personal_info.save()

                        volun_info = JR_VOLUNTEER(
                            VOLUNTEER_PH_NO=current_user_model, VOLUNTEER_LEVEL_ID=level,
                            VOLUNTEER_NAME=name, VOLUNTEER_TITLE=title,
                            VOLUNTEER_EMAIL=email, VOLUNTEER_GENDER=gender, VOLUNTEER_DOB=date_birth,
                            VOLUNTEER_IS_CERTIFIED=is_certified
                        )

                        volun_info.save()

                        token = Token.objects.create(user=current_user_model)

                        volun_dnd = JR_VOLUNTEER_DND(
                            VOLUNTEER_PH_NO=current_user_model,
                            DND_FL=False
                        )

                        volun_dnd.save()

                        v_loc = Point(12.9716, 77.5946)

                        volun_loc = VOLUNTEER_LOC(
                            VOLUNTEER_PH_NO=current_user_model,
                            VOLUNTEER_CURR_LOC=v_loc
                        )

                        volun_loc.save()

                        otp_info = OTPModel(
                            phone=phone, otp=0000,
                            is_verified=False
                        )

                        otp_info.save()

                        user_fcm_info = FCMDevices(
                            USER_PH_NO=current_user_model,
                            DEVICE_TOKEN="0"
                        )

                        user_fcm_info.save()

            return render(request, 'file_upload/details.html', {'upload_dat': upload_dat})
    context = {"form": form, }
    return render(request, 'file_upload/upload.html', context)

