from geopy.geocoders import Nominatim
longlat = [[52.407052],[-1.473959]]
varlola1 = str(longlat[0][0])
varlola2 = ","
varlola3 = str(longlat[1][0])
varlola = varlola1+varlola2+varlola3
print(varlola)
geolocator = Nominatim(user_agent="JH")
location = geolocator.reverse(varlola)
print(location.address)