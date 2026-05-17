from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
CITY = os.getenv("CITY", "london")
LANG = os.getenv("LANG", "en")


def fetch_weather_data(city=CITY, lang=LANG):
    headers = {
        "Authorization": f"apikey {API_KEY}"
    }
    params = {
        "city": city,
        "lang": lang
    }
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


weather_data = fetch_weather_data()
print(weather_data)
