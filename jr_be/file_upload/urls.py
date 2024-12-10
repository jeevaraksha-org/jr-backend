from django.urls import path
from . import views
from jr_be import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.upload_excel_csv, name='upload_file'),
]

if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)