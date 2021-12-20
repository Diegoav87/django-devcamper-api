from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt
from geopy import distance

geolocator = Nominatim(user_agent="addressGeolocator")


def geolocate(address):
    geolocation = geolocator.geocode(address)

    if geolocation == None:
        return None

    lat = geolocation.latitude
    lng = geolocation.longitude
    return lng, lat


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def calculate_distance(center_point, test_point, radius):
    dis = distance.distance(center_point, test_point).km

    if dis <= radius:
        return True
    else:
        return False
