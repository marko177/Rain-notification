import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

weather_parameters = {
    "lat": float(os.environ.get("LAT")),
    "lon": float(os.environ.get("LON")),
    "units": "metric",
    "exclude": "current,minutely,daily,alerts",
    "appid": os.environ.get("OWM_API_KEY")
}

request_weather = requests.get("https://api.openweathermap.org/data/2.5/onecall?", params=weather_parameters)

weather_data = request_weather.json()

if [i["weather"][0]["id"] for i in weather_data["hourly"][:12] if i["weather"][0]["id"] < 700]:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages.create(
        body="Bring an umbrella!",
        from_=os.environ.get("FROM_NUM"),
        to=os.environ.get("TO_NUM")
    )
else:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages.create(
        body="It's not going to rain today!",
        from_=os.environ.get("FROM_NUM"),
        to=os.environ.get("TO_NUM")
    )
