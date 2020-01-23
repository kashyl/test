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


async def fetch_weather_data():
    """Fetches the data from the openweathermap.org api asynchronously in weather_resp"""
    while True:  # so the loop continues after one run; use this as long as async call is performed inside
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&APPID={weatherKey}') \
                    as weather_req:
                weather_resp = json.loads(await weather_req.text())
                pprint(weather_resp)
                # converts the default Kelvin to Celsius °C
                celsius = round(weather_resp['main']['temp'] - 273.15, 2)
        await asyncio.sleep(300)  # the time between API calls

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(fetch_weather_data())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()
