

import os
from dotenv import load_dotenv

load_dotenv()


class AppConfig:
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    CITIES: list[str] = [
        c.strip() for c in os.getenv("CITIES", "Nairobi").split(",")
    ]
    SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL", "60"))

    KAFKA_BOOTSTRAP_SERVERS = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "weather-data")

    CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
    CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
    CASSANDRA_KEYSPACE = os.getenv(
        "CASSANDRA_KEYSPACE", "weather_pipeline")
    CASSANDRA_TABLE = os.getenv("CASSANDRA_TABLE", "weather_records")

    def validate(self) -> None:
        """Raise early if critical config is missing."""
        if not self.OPENWEATHER_API_KEY:
            raise ValueError(
                "OPENWEATHER_API_KEY is not set. "
            )


settings = AppConfig()
