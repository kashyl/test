"""module docstring here"""
import os  # Miscellaneous operating system interfaces, https://docs.python.org/3/library/os.html
from datetime import datetime
# pprint = pretty print with indentation, good for JSON files so not everything is on the same line
from pprint import pprint  # so we can do pprint(stuff) instead of pprint.pprint(stuff)
import asyncio
import aiohttp  # fetch data from urls asynchronously (compared to import requests which is sync)
import json
import urllib  # converts strings to url format (needed in case of special characters)
import urllib.parse

weatherKey = os.environ['WEATHER_API_KEY']  # Fetch OpenWeatherMap API key from environmental variables
location = "Hong Kong"


async def weather_command(f_arg=' ', *args):
    """Fetches the data from the openweathermap.org api asynchronously in weather_resp"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&APPID={weatherKey}') \
                as weather_req:
            weather_resp = json.loads(await weather_req.text())
            pprint(weather_resp)
            # converts the default Kelvin to Celsius °C
            celsius = round(weather_resp['main']['temp'] - 273.15, 2)


loop = asyncio.events.new_event_loop()
loop.run_until_complete(weather_command())
