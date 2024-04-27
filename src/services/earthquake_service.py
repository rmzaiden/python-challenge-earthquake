from datetime import datetime, timezone

import requests
from fastapi import HTTPException
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


class EarthquakeService:
    """
    A class that provides methods to fetch earthquake data, process the data, and retrieve a message about the search.

    Attributes:
        geolocator (Nominatim): A geolocator object used for geocoding and reverse geocoding.
        api_url (str): The URL of the earthquake data API.

    Methods:
        fetch_earthquake_data: Fetches earthquake data from the API.
        get_city_coordinates: Retrieves the coordinates (latitude and longitude) of a city.
        reverse_geocode: Performs reverse geocoding to get the address of a location.
        convert_date: Converts a date string to a readable format.
        convert_timestamp_to_readable_date: Converts a timestamp to a readable date format.
        process_earthquake_data: Processes earthquake data and returns the closest earthquake to a city.

    """

    def __init__(self):
        self.geolocator = Nominatim(user_agent="my_unique_geocoder")
        self.api_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    def fetch_earthquake_data(self, starttime, endtime):
        """
        Fetches earthquake data from the API.

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
        Retrieves the coordinates (latitude and longitude) of a city.

        Args:
            city_name (str): The name of the city.

        Returns:
            tuple: The latitude and longitude of the city.

        Raises:
            ValueError: If the city is not found.

        """
        location = self.geolocator.geocode(city_name)
        if location:
            return (location.latitude, location.longitude)
        else:
            raise ValueError(f"Coordinates not found for {city_name} city.")

    def reverse_geocode(self, latitude, longitude):
        """
        Performs reverse geocoding to get the address of a location.

        Args:
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.

        Returns:
            str: The address of the location.

        """
        location = self.geolocator.reverse((latitude, longitude), exactly_one=True)
        return location.address if location else "Unknown location"

    def convert_date(self, date_str):
        """
        Converts a date string to a readable format.

        Args:
            date_str (str): The date string in the format "YYYY-MM-DD".

        Returns:
            str: The date string in the format "Month DD, YYYY".

        """
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")

    def convert_timestamp_to_readable_date(self, timestamp_ms):
        """
        Converts a timestamp to a readable date format.

        Args:
            timestamp_ms (int): The timestamp in milliseconds.

        Returns:
            str: The readable date string in the format "Month DD".

        """
        return datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc).strftime(
            "%B %d"
        )

    def process_earthquake_data(self, query):
        """
        Processes earthquake data and returns the closest earthquake to a city.

        Args:
            query (Query): An object containing the city name, start date, and end date.

        Returns:
            dict: A dictionary containing the result message.

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
        start_date = self.convert_date(query.start_date)
        end_date = self.convert_date(query.end_date)
        if closest_earthquake:
            mag = closest_earthquake["properties"]["mag"]
            eq_coordinates = closest_earthquake["geometry"]["coordinates"]
            time_ms = closest_earthquake["properties"]["time"]
            earthquake_date = self.convert_timestamp_to_readable_date(time_ms)
            nearest_city = self.reverse_geocode(eq_coordinates[1], eq_coordinates[0])
            state_abbreviation = (
                f"{query.state_abbreviation}" if query.state_abbreviation else ""
            )
            return {
                "message": f"Result for {query.city_name},{state_abbreviation} between {start_date} and {end_date}: The closest earthquake to {query.city_name} was an M {mag} - {nearest_city} on {earthquake_date}"
            }
        return {
            "message": f"No results found for {query.city_name} between {start_date} and {end_date}."
        }
