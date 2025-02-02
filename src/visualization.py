from geopy.geocoders import Nominatim

def city_changed(new_city):
    return new_city != getattr(city_changed, "last_city", None)

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="map-app")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        # W przypadku braku miasta, zwróć domyślne współrzędne
        return 51.0866, 16.9748  # Wrocław, Polska