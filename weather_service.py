"""Weather service for getting current weather information."""
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from typing import Dict, Any, Optional
import os
from datetime import datetime


class WeatherService:
    """Service for fetching weather data from Open-Meteo API."""
    
    def __init__(self):
        """Initialize the weather service."""
        # Setup the Open-Meteo API client with cache and retry on error
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
        
        # Default location (Cairo, Egypt)
        self.default_latitude = 30.0626
        self.default_longitude = 31.2497
        self.default_timezone = "Africa/Cairo"
    
    def get_current_weather(self, latitude: Optional[float] = None, longitude: Optional[float] = None) -> Dict[str, Any]:
        """Get current weather information."""
        try:
            # Use default coordinates if not provided
            lat = latitude or self.default_latitude
            lon = longitude or self.default_longitude
            
            print(f"Fetching weather for coordinates: {lat}°N, {lon}°E")
            
            # Make sure all required weather variables are listed here
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "hourly": ["temperature_2m", "rain", "visibility", "relative_humidity_2m", "wind_speed_10m"],
                "timezone": self.default_timezone,
            }
            
            responses = self.openmeteo.weather_api(url, params=params)
            response = responses[0]
            
            # Get current weather (first hour of data)
            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
            hourly_rain = hourly.Variables(1).ValuesAsNumpy()
            hourly_visibility = hourly.Variables(2).ValuesAsNumpy()
            hourly_humidity = hourly.Variables(3).ValuesAsNumpy()
            hourly_wind_speed = hourly.Variables(4).ValuesAsNumpy()
            
            # Get current values (first hour)
            current_temp = float(hourly_temperature_2m[0])
            current_rain = float(hourly_rain[0])
            current_visibility = float(hourly_visibility[0])
            current_humidity = float(hourly_humidity[0])
            current_wind_speed = float(hourly_wind_speed[0])
            
            # Format weather data
            weather_data = {
                "location": {
                    "latitude": response.Latitude(),
                    "longitude": response.Longitude(),
                    "elevation": response.Elevation(),
                    "timezone": response.Timezone(),
                    "timezone_abbreviation": response.TimezoneAbbreviation()
                },
                "current_weather": {
                    "temperature": current_temp,
                    "rain": current_rain,
                    "visibility": current_visibility,
                    "humidity": current_humidity,
                    "wind_speed": current_wind_speed
                },
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"SUCCESS: Weather data retrieved for {response.Latitude()}°N {response.Longitude()}°E")
            return weather_data
            
        except Exception as e:
            print(f"ERROR: Failed to fetch weather data: {str(e)}")
            return {
                "error": f"Failed to fetch weather data: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_weather_summary(self, latitude: Optional[float] = None, longitude: Optional[float] = None) -> str:
        """Get a human-readable weather summary."""
        weather_data = self.get_current_weather(latitude, longitude)
        
        if "error" in weather_data:
            return f"Weather data unavailable: {weather_data['error']}"
        
        current = weather_data["current_weather"]
        location = weather_data["location"]
        
        # Create a friendly weather summary
        temp_c = current["temperature"]
        rain_mm = current["rain"]
        visibility_km = current["visibility"] / 1000  # Convert to km
        humidity = current["humidity"]
        wind_speed = current["wind_speed"]
        
        summary = f"""Current weather in {str(location['timezone'])}:
Temperature: {temp_c:.1f} degrees Celsius
Rain: {rain_mm:.1f}mm
Visibility: {visibility_km:.1f}km
Humidity: {humidity:.1f}%
Wind Speed: {wind_speed:.1f}km/h
Location: {location['latitude']:.4f}N, {location['longitude']:.4f}E"""
        
        return summary


def get_weather_service() -> WeatherService:
    """Get a weather service instance."""
    return WeatherService()
