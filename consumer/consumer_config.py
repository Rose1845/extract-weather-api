from kafka import KafkaConsumer
import json
from config.app_config import settings
from config.cassandra_config import connect_cassandra, prepare_insert, insert_weather
from config.log import log


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
    insert_record_data = prepare_insert(session)
    consumer = create_consumer()

    try:
        for message in consumer:
            record = message.value

            log.info(f"record: {record}")
            try:
                insert_weather(session, insert_record_data, record)
                consumer.commit()
                log.info(
                    f"{record['city']} | "
                    f"{record['timestamp']} | "
                    f"{record['temperature']}°C | "
                    f"{record['description']}"
                )

            except Exception as e:
                log.error(
                    "Failed to write record for %s: %s",
                    record.get("city", "?"),
                    e,
                )
    except Exception as e:
        log.error(
            "An error occured: %s: %s"
        )

    finally:
        consumer.close()
        log.info("Consumer closed.")


if __name__ == "__main__":
    exceute_consumer()
