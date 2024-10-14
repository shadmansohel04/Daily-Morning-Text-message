from twilio.rest import Client
from datetime import time, timedelta, datetime
import requests
import datetime as dt
import schedule
import time as tm
import json
import googlemaps

googleAPIKey = 'APIKEY'

#COMMUTE DESCRIPTION

gmapsClient = googlemaps.Client(googleAPIKey)
source = "ADDRESS"
destination = "WORK"

direction_result = gmapsClient.directions(source, destination, mode="transit", avoid="ferries", departure_time ="now")
commute = direction_result[0]['legs'][0]['duration']
commute_time = commute['text']
commute_description = f"Your commute to work is {commute_time}."

account_sid = 'SID'
auth_token = 'TOKEN'
twilio_number = 'TWILIONUMB'
my_phone_number = 'MYNUMB'

API_KEY = 'APIKEY2'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'
CITY = "MYCITY"

url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY

def kelvin_to_celcius(kelvin):
    celcius = kelvin - 273.15
    return celcius

response = requests.get(url).json()

#TEMPERATURE DESCRIPTION

temp_kelvin = response['main']['temp']
temp_celcius = round(kelvin_to_celcius(temp_kelvin), 2)

feels = round(kelvin_to_celcius(response['main']['feels_like']), 2)

temp_description = f"the current tempurature in {CITY} is {temp_celcius} degrees celcius, but it feels like {feels}. "

#DAY DESCRIPTION

humidity = response['main']['humidity']
if (humidity <= 55):
    humidity = f"It's pretty dry today with a humidity of {humidity}. "
elif (humidity > 55 and humidity < 65):
    humidity = f"It's a little sticky with a humidity of {humidity}. "
else:
    humidity = f"It's really sticky with a humidity of {humidity}. "

description = response['weather'][0]['description']
description = f"You can expect {description}."

day_description = humidity + description

client = Client(account_sid, auth_token)


def send():
    message = client.messages.create(
        body=f"Hello Shadman, {temp_description} {day_description} {commute_description}",
        from_=twilio_number,
        to=my_phone_number
    )
    print(message.body)

send()
