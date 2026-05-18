
# from transform.weather_transform import transform_weather_data
# from extract.api import fetch_weather_data
# from load.insert_records import insert_weather_data


# def run_pipeline():
#     weather_raw = fetch_weather_data()
#     weather_clean = transform_weather_data(weather_raw)
#     for day in weather_clean:
#         insert_weather_data(day)


# if __name__ == "__main__":
#     run_pipeline()
# main.py
import threading
from producer.producer_config import execute_producer as run_producer
from consumer.consumer_config import exceute_consumer as run_consumer

if __name__ == "__main__":
    producer_thread = threading.Thread(target=run_producer, name="Producer")
    consumer_thread = threading.Thread(target=run_consumer, name="Consumer")

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
