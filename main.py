import requests
import smtplib
import os


MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")


# API endpoints and credentials
# Note: In production code, it is safer to store API keys in environment variables
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
geo_coder_endpoint = "http://api.openweathermap.org/geo/1.0/zip"
api_key = os.environ.get("OWM_API_KEY")
my_zip = os.environ.get("MY_ZIP")


# ---------------------------------------------------------
# 1. Geocoding Setup: Convert Zip Code to Coordinates
# ---------------------------------------------------------
geo_coder_parameters = {
    "zip": [my_zip, "US"],
    "appid": api_key,
}

# Fetch latitude and longitude
response_2 = requests.get(url=geo_coder_endpoint, params=geo_coder_parameters)
response_2.raise_for_status()
geo_data = response_2.json()

MY_LAT = geo_data["lat"]
MY_LNG = geo_data["lon"]

# ---------------------------------------------------------
# 2. Weather Setup: Fetch Forecast Data
# ---------------------------------------------------------
# Set parameters for the weather API request (fetching next 4 intervals)
weather_parameters = {
    "lat": MY_LAT,
    "lon": MY_LNG,
    "appid": api_key,
    "cnt": 4,
}

# Fetch the weather forecast data
response = requests.get(url=OWM_Endpoint, params=weather_parameters)
response.raise_for_status()
weather_data = response.json()


# ---------------------------------------------------------
# 3. Forecast Evaluation
# ---------------------------------------------------------
def going_to_rain():
    """Checks the upcoming forecast intervals for rain condition codes."""
    will_rain = False
    for hour_data in weather_data["list"]:
        condition_code = hour_data["weather"][0]["id"]

        # OpenWeatherMap condition codes under 600 indicate rain, drizzle, or thunderstorms
        if int(condition_code) < 600:
            will_rain = True

    return will_rain


# Output the forecast result
if going_to_rain():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="t.grimes41@gmail.com",
                msg="Subject:Rain Alert\n\n It is going to rain")
