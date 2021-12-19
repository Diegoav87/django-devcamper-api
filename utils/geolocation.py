from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="addressGeolocator")


def geolocate(address):
    geolocation = geolocator.geocode(address)

    if geolocation == None:
        return None

    lat = geolocation.latitude
    lng = geolocation.longitude
    pnt = Point(lng, lat, srid=4326)
    return pnt
