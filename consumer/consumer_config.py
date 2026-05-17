from kafka import KafkaConsumer
import json
from config.app_config import settings
from config.cassandra_config import connect_cassandra, prepare_insert, insert_weather


def create_consumer():
    return KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="weather-cassandra-consumer",
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        value_deserializer=lambda b: json.loads(b.decode("utf-8")),
        key_deserializer=lambda b: b.decode("utf-8") if b else None,
    )


def exceute_consumer():
    session = connect_cassandra()
    consumner = create_consumer()
