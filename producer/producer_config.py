
from config.app_config import settings
from config.log import log
from kafka import KafkaProducer
import json
import time
import sys
import os
from faker import Faker

from extract.api import fetch_weather
fake = Faker()
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def create_producer():
    return KafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
        acks="all",
        retries=3,
    )


def publish(producer, weather):
    producer.send(
        topic=settings.KAFKA_TOPIC,
        key=weather["city"],
        value=weather,
    )


def execute_producer() -> None:
    settings.validate()
    log.info("Starting Weather Producer")
    log.info("Cities : %s", settings.CITIES)
    log.info("Topic  : %s", settings.KAFKA_TOPIC)
    log.info("Interval: %ds", settings.SLEEP_INTERVAL)

    producer = create_producer()
    log.info("Connected to Kafka at %s", settings.KAFKA_BOOTSTRAP_SERVERS)

    try:
        while True:
            for city in settings.CITIES:
                log.info("Fetching weather for %s", city)
                weather = fetch_weather(city)

                if weather:
                    publish(producer, weather)
                    log.info(
                        "Published  %s | %.1f°C | %s",
                        weather["city"],
                        weather["temperature"],
                        weather["description"],
                    )
            producer.flush()
            log.info("Sleeping %ds before next poll …\n",
                     settings.SLEEP_INTERVAL)
            time.sleep(settings.SLEEP_INTERVAL)

    except KeyboardInterrupt:
        log.info("Shutting down producer …")
    finally:
        producer.close()
        log.info("Producer closed.")


if __name__ == "__main__":
    execute_producer()
