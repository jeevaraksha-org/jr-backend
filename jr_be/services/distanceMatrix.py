import googlemaps

gmaps = googlemaps.Client(key='REDACTED')

origins = {"lat": 17.3850, "lng": 78.4867}
destinations = {"lat": 12.9716, "lng": 77.5946}

distance_mat = gmaps.distance_matrix(origins, destinations)

print(distance_mat)