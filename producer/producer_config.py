from kafka import KafkaProducer
import json
import time
from faker import Faker
from config.app_config import settings
fake = Faker()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
topic = 'fake_users'


def create_producer():
    return KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


def publish(producer, weather):
    producer.send(
        topic=settings.KAFKA_TOPIC,
        key=weather["city"],
        value=weather,
    )


def generate_fake_users():
    return {
        'name': fake.name(),
        'address': fake.address()
    }


while True:
    user = generate_fake_users()
    producer.send(topic, user)
    print(f"sent: {user}")
    time.sleep(2)
