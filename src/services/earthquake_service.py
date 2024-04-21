from datetime import datetime, timezone
import requests
from fastapi import HTTPException
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class EarthquakeService:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="my_unique_geocoder")
        self.api_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    def fetch_earthquake_data(self, starttime, endtime):
        params = {
            'format': 'geojson',
            'starttime': starttime,
            'endtime': endtime,
            'minmagnitude': 5,
            'orderby': 'magnitude'
        }
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve earthquake data.")
    
    def get_city_coordinates(self, city_name):
        location = self.geolocator.geocode(city_name)
        if location:
            return (location.latitude, location.longitude)
        else:
            raise ValueError("City not found")

    def reverse_geocode(self, latitude, longitude):
        location = self.geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            return location.address
        else:
            return "Unknown location"
    
    def convert_timestamp_to_readable_date(self, timestamp_ms):
        return datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc).strftime('%B %d')

    def process_earthquake_data(self, query):
        city_coordinates = self.get_city_coordinates(query.city_name)
        earthquake_data = self.fetch_earthquake_data(query.start_date, query.end_date)
        closest_earthquake = None
        min_distance = float('inf')
        for earthquake in earthquake_data.get("features", []):
            mag = earthquake["properties"]["mag"]
            eq_coordinates = earthquake["geometry"]["coordinates"]
            eq_point = (eq_coordinates[1], eq_coordinates[0])
            distance = geodesic(city_coordinates, eq_point).kilometers
            if distance < min_distance:
                min_distance = distance
                closest_earthquake = earthquake
        if closest_earthquake:
            mag = closest_earthquake["properties"]["mag"]
            eq_coordinates = closest_earthquake["geometry"]["coordinates"]
            time_ms = closest_earthquake["properties"]["time"]
            earthquake_date = self.convert_timestamp_to_readable_date(time_ms)
            nearest_city = self.reverse_geocode(eq_coordinates[1], eq_coordinates[0])
            return f"The closest earthquake to {query.city_name} was an M {mag} - {nearest_city} on {earthquake_date}"
        return "No results found."
