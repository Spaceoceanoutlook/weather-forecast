import requests
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('API_KEY')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Cache-Control': 'no-cache'
}


def city_ending(c: str) -> str:
    c = c.lower()
    if c[-1] == 'а':
        return c[:-1] + 'е'
    if c[-1] == 'ы':
        return c[:-1] + 'ах'
    if c[-1] in ["я", "ь"]:
        return c[:-1] + 'и'
    if c[-1] in ["у", "и", "е", "о"]:
        return c
    return c + 'е'


def get_temperature(city_name: str) -> str:
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&appid={API_KEY}&units=metric'
    response = requests.get(url, headers=headers)
    temp = response.json()['main']['temp']
    return f'В {city_ending(city_name).capitalize()} сейчас {round(temp)} °C'