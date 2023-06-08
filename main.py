import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv
# More info on Python Anywhere + Twilio Free Tier fix: https://help.pythonanywhere.com/pages/TwilioBehindTheProxy/
# from twilio.http.http_client import TwilioHttpClient

url = "https://api.openweathermap.org/data/2.5/forecast"
load_dotenv("venv/.env")
weather_api_key = os.getenv("OWM_API_KEY")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = os.getenv("TWILIO_NUM")
to_number = os.getenv("TO_NUMBER")

test_lat = 21.481291
test_long = 109.120163
home_lat = 37.762098
home_long = -122.443438

parameters = {
    "lat": test_lat,
    "lon": test_long,
    "appid": weather_api_key,
}

response = requests.get(url=url, params=parameters)
response.raise_for_status()

weather_forecast = response.json()["list"]

for three_hour in weather_forecast[0:4]:
    if three_hour["weather"][0]["id"] < 700:
        # Use commented code below if using Python Anywhere with Twilio's free tier:
        # proxy_client = TwilioHttpClient()
        # proxy_client.session.proxies = {'https': os.environ['https_proxy']}
        # client = Client(account_sid, auth_token, http_client=proxy_client)
        message = client.messages.create(
            body="It's going to rain today. Remember to bring an ☔",
            from_=twilio_number,
            to=to_number
        )
        break
print(message.status)
