
CREATE KEYSPACE IF NOT EXISTS weather_pipeline
    WITH replication = {
        'class': 'SimpleStrategy',
        'replication_factor': 1
    }
    AND durable_writes = true;

USE weather_pipeline;

CREATE TABLE IF NOT EXISTS weather_records (
    id          UUID,
    city        TEXT,
    country     TEXT,
    timestamp   TIMESTAMP,
    temperature FLOAT,
    feels_like  FLOAT,
    humidity    INT,
    pressure    INT,
    wind_speed  FLOAT,
    weather     TEXT,
    description TEXT,
    PRIMARY KEY ((city), timestamp, id)
) WITH CLUSTERING ORDER BY (timestamp DESC, id ASC)
  AND default_time_to_live = 2592000  
  AND comment = 'Real-time weather readings streamed from OpenWeather API via Kafka';

