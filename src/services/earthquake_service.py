from datetime import datetime, timezone

import requests
from fastapi import HTTPException
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


class EarthquakeService:
    """
    A class that provides methods to fetch earthquake data, process earthquake data, and perform geolocation operations.
    """

    def __init__(self):
        self.geolocator = Nominatim(user_agent="my_unique_geocoder")
        self.api_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    def fetch_earthquake_data(self, starttime, endtime):
        """
        Fetches earthquake data from the USGS Earthquake Catalog API.

        Args:
            starttime (str): The start time of the earthquake data query.
            endtime (str): The end time of the earthquake data query.

        Returns:
            dict: The earthquake data in GeoJSON format.

        Raises:
            HTTPException: If the API request fails.
        """
        params = {
            "format": "geojson",
            "starttime": starttime,
            "endtime": endtime,
            "minmagnitude": 5,
            "orderby": "magnitude",
        }
        response = requests.get(self.api_url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to retrieve earthquake data.",
            )

    def get_city_coordinates(self, city_name):
        """
        Retrieves the latitude and longitude coordinates of a given city.

        Args:
            city_name (str): The name of the city.

        Returns:
            tuple: A tuple containing the latitude and longitude coordinates of the city.

        Raises:
            ValueError: If the city is not found.
        """
        location = self.geolocator.geocode(city_name)
        if location:
            return (location.latitude, location.longitude)
        else:
            raise ValueError("City not found")

    def reverse_geocode(self, latitude, longitude):
        """
        Performs reverse geocoding to retrieve the address of a given latitude and longitude.

        Args:
            latitude (float): The latitude coordinate.
            longitude (float): The longitude coordinate.

        Returns:
            str: The address corresponding to the given coordinates.

        Returns:
            str: "Unknown location" if the location is not found.
        """
        location = self.geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            return location.address
        else:
            return "Unknown location"

    def convert_timestamp_to_readable_date(self, timestamp_ms):
        """
        Converts a timestamp in milliseconds to a readable date format.

        Args:
            timestamp_ms (int): The timestamp in milliseconds.

        Returns:
            str: The readable date format.
        """
        return datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc).strftime(
            "%B %d"
        )

    def process_earthquake_data(self, query):
        """
        Processes earthquake data to find the closest earthquake to a given city.

        Args:
            query (Query): An object containing the city name, start date, and end date.

        Returns:
            str: A string describing the closest earthquake to the given city.

        Returns:
            str: "No results found." if no earthquake data is available.
        """
        city_coordinates = self.get_city_coordinates(query.city_name)
        earthquake_data = self.fetch_earthquake_data(query.start_date, query.end_date)
        closest_earthquake = None
        min_distance = float("inf")
        for earthquake in earthquake_data.get("features", []):
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
            return {
                "message": f"The closest earthquake to {query.city_name} was an M {mag} - {nearest_city} on {earthquake_date}"
            }
        return {"message": "No results found."}
