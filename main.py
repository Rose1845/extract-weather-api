
from transform.weather_transform import transform_weather_data
from extract.api import fetch_weather_data
from load.insert_records import insert_weather_data


def run_pipeline():
    weather_raw = fetch_weather_data()
    weather_clean = transform_weather_data(weather_raw)
    for day in weather_clean:
        insert_weather_data(day)


if __name__ == "__main__":
    run_pipeline()
