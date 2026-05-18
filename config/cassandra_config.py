
from config.app_config import settings
from cassandra.cluster import Cluster, Session
from cassandra.policies import RoundRobinPolicy
from cassandra.query import SimpleStatement
import logging
import uuid
from datetime import datetime, timezone
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def connect_cassandra() -> Session:
    cluster = Cluster(
        contact_points=[settings.CASSANDRA_HOST],
        port=settings.CASSANDRA_PORT,
        load_balancing_policy=RoundRobinPolicy(),
    )

    session = cluster.connect()

    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {settings.CASSANDRA_KEYSPACE}
        WITH replication = {{
            'class': 'SimpleStrategy',
            'replication_factor': 1
        }}
    """)

    session.set_keyspace(settings.CASSANDRA_KEYSPACE)

    session.execute(f"""
        CREATE TABLE IF NOT EXISTS {settings.CASSANDRA_TABLE} (
            id UUID PRIMARY KEY,
            city TEXT,
            country TEXT,
            timestamp TIMESTAMP,
            temperature FLOAT,
            feels_like FLOAT,
            humidity INT,
            pressure INT,
            wind_speed FLOAT,
            weather TEXT,
            description TEXT
        )
    """)

    log.info(
        "Connected to Cassandra at %s:%d keyspace=%s",
        settings.CASSANDRA_HOST,
        settings.CASSANDRA_PORT,
        settings.CASSANDRA_KEYSPACE,
    )

    return session


def connect_cassandra1() -> Session:
    """
    Connect to Cassandra and return an active session bound to the keyspace.
    Retries are handled by the driver internally.
    """
    cluster = Cluster(
        contact_points=[settings.CASSANDRA_HOST],
        port=settings.CASSANDRA_PORT,
        load_balancing_policy=RoundRobinPolicy(),
    )
    session = cluster.connect(settings.CASSANDRA_KEYSPACE)
    log.info(
        "Connected to Cassandra at %s:%d  keyspace=%s",
        settings.CASSANDRA_HOST,
        settings.CASSANDRA_PORT,
        settings.CASSANDRA_KEYSPACE,
    )
    return session


def prepare_insert(session: Session):
    """
    Pre-compile the INSERT statement once so the driver can reuse the
    query plan on every subsequent execution (better performance).
    """
    cql = f"""
        INSERT INTO {settings.CASSANDRA_TABLE} (
            id,
            city,
            country,
            timestamp,
            temperature,
            feels_like,
            humidity,
            pressure,
            wind_speed,
            weather,
            description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    return session.prepare(cql)


def insert_weather(session: Session, prepared, record: dict):
    """Execute one INSERT for a single weather record."""
    session.execute(
        prepared,
        (
            uuid.uuid4(),
            record["city"],
            record["country"],
            datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00")),
            float(record["temperature"]),
            float(record["feels_like"]),
            int(record["humidity"]),
            int(record["pressure"]),
            float(record["wind_speed"]),
            record["weather"],
            record["description"],
        ),
    )
