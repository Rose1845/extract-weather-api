from config.app_config import settings
from config.log import log
from datetime import datetime, timezone
from dotenv import load_dotenv
import requests

load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city):
    print(f"BASE_URL: {BASE_URL}")
    params = {
        "q": city,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # df = pd.DataFrame(data)
        # df.head()

        # print(df.head())

        return {
            "city":        data["name"],
            "country":     data["sys"]["country"],
            "timestamp":   datetime.now(timezone.utc).isoformat(),
            "temperature": data["main"]["temp"],
            "feels_like":  data["main"]["feels_like"],
            "humidity":    data["main"]["humidity"],
            "pressure":    data["main"]["pressure"],
            "wind_speed":  data["wind"]["speed"],
            "weather":     data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
        }

    except requests.exceptions.HTTPError as e:
        log.error("HTTP error fetching weather for %s: %s", city, e)
    except requests.exceptions.ConnectionError:
        log.error("Network error could not reach OpenWeather API for %s", city)
    except requests.exceptions.Timeout:
        log.error("Request timed out for %s", city)
    except (KeyError, ValueError) as e:
        log.error("Unexpected API response format for %s: %s", city, e)

    return None
