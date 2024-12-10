from django.contrib.gis.geos import Point
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from core.models import VOLUNTEER_LOC

user_latitude = 12.971599
user_longitude = 77.594566

user_loc = Point(user_longitude, user_latitude, srid=4326)
queryset = VOLUNTEER_LOC.objects.annotate(distance=Distance('VOLUNTEER_CURR_LOC', user_loc)).order_by('distance')

print(queryset)