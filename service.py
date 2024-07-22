import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry
import datetime


def get_time() -> str:
    return datetime.datetime.now().strftime("%d %B %Y")


def get_coord(user_city: str) -> dict | str:
    params = {"name": user_city,
              "language": "ru",
              "format": "json",
              "count": 1,
              }
    url = "https://geocoding-api.open-meteo.com/v1/search"
    response = requests.get(url, params=params)
    try:
        coord = response.json()["results"][0]
    except KeyError:
        return f'Нет информации о погоде в городе "{user_city}"'
    return {"latitude": coord["latitude"],
            "longitude": coord["longitude"],
            "country": coord["country"],
            "population": coord["population"]}


def get_temperature(city: str) -> tuple | str:
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    open_meteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    coord = get_coord(city)
    if isinstance(coord, str):
        return coord
    params = {
        "latitude": coord["latitude"],
        "longitude": coord["longitude"],
        "hourly": ["temperature_2m"],
        "forecast_days": 1
    }
    responses = open_meteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()
    time_and_temp = []
    country = coord["country"]
    population = coord["population"]
    for c, t in enumerate(hourly.Variables(0).ValuesAsNumpy()):
        data = (f"{c}-00", round(t))
        time_and_temp.append(data)
    return time_and_temp, country, population
