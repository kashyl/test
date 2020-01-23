"""module docstring here"""
import os  # Miscellaneous operating system interfaces, https://docs.python.org/3/library/os.html
from datetime import datetime
# pprint = pretty print with indentation, good for JSON files so not everything is on the same line
from pprint import pprint  # so we can do pprint(stuff) instead of pprint.pprint(stuff)
from datetime import datetime
import asyncio
import aiohttp  # fetch data from urls asynchronously (compared to import requests which is sync)
import json
import urllib  # converts strings to url format (needed in case of special characters)
import urllib.parse
import pymongo as pymongo

"""Get environment variables"""
dbUser = os.environ['DB_USER']
dbPass = os.environ['DB_PASS']
dbPassURL = urllib.parse.quote(dbPass)
weatherKey = os.environ['WEATHER_API_KEY']  # Fetch OpenWeatherMap API key from environment variables
"""End environment variables"""

"""Connect to MongoDB"""
client = pymongo.MongoClient(f'mongodb+srv://{dbUser}:{dbPassURL}'
                             f'@issf2020hk-la5xb.gcp.mongodb.net/test?retryWrites=true&w=majority')
db = client["mydb"]
users_col = db["users"]
weather_col = db["regional_weather"]
print(db.list_collection_names())


async def regional_weather_data():
    """Fetches the data from the openweathermap.org api asynchronously in weather_resp"""
    while True:  # so the loop continues after one run; use this as long as async call is performed inside
        location = "Hong Kong"
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&APPID={weatherKey}') \
                    as weather_req:
                weather_resp = json.loads(await weather_req.text())  # Converts the request data into JSON format
                celsius = round(weather_resp['main']['temp'] - 273.15, 2)  # converts the default Kelvin to Celsius °C
                # pprint(weather_resp)  # for debugging
                weather_col.insert_one(weather_resp)  # Store to database
                print("Stored regional data @", end=" ")  # status message
                print(datetime.now(), end=" ")  # print timestamp
                print(f'- {weather_resp["name"]}: {celsius}°C, {weather_resp["weather"][0]["description"]} ')

        await asyncio.sleep(30)  # the time between API calls


"""Start of asyncio event loop"""
loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(regional_weather_data())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()
"""End of loop"""
