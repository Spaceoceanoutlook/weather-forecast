import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry


def get_coord(user_name: str) -> dict | str:
    params = {"name": user_name,
              "language": "ru",
              "format": "json",
              "count": 1,
              }
    url = "https://geocoding-api.open-meteo.com/v1/search"
    response = requests.get(url, params=params)
    try:
        coord = response.json()["results"][0]
    except KeyError:
        return "Нет информации о погоде об этом городе"
    return {"latitude": coord["latitude"], "longitude": coord["longitude"]}


def get_temperature(city: str) -> list | str:
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
    for c, t in enumerate(hourly.Variables(0).ValuesAsNumpy()):
        data = (f"{c}-00", round(t))
        time_and_temp.append(data)
    return time_and_temp


if __name__ == "__main__":
    print(get_temperature("Пермь"))
