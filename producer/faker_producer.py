from kafka import KafkaProducer
import json
import time
from faker import Faker

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
topic = 'fake_users'


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
