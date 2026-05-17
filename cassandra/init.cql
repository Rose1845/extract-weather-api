-- cassandra/init.cql
-- ─────────────────────────────────────────────────────────────────────────────
-- Run once to bootstrap the keyspace and table.
-- The Docker Compose setup mounts this file and Cassandra executes it on start.
-- You can also run it manually:  cqlsh < cassandra/init.cql
-- ─────────────────────────────────────────────────────────────────────────────

-- Create the keyspace with SimpleStrategy (fine for local/single-node dev).
-- For multi-node production use NetworkTopologyStrategy and set a replication
-- factor matching your cluster size.
CREATE KEYSPACE IF NOT EXISTS weather_pipeline
    WITH replication = {
        'class': 'SimpleStrategy',
        'replication_factor': 1
    }
    AND durable_writes = true;

USE weather_pipeline;

-- ── Main table ────────────────────────────────────────────────────────────────
--
-- Partition key : city
--   All readings for one city are stored together on the same Cassandra node.
--   Queries like "give me all readings for Nairobi" are served from a single
--   partition — no cross-node scatter needed.
--
-- Clustering key: timestamp DESC
--   Within a city's partition, rows are ordered newest-first so that
--   `LIMIT 10` immediately returns the most recent readings without a sort.
--
-- id (UUID): tie-breaker so duplicate timestamps never silently overwrite data.
-- ─────────────────────────────────────────────────────────────────────────────
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
  AND default_time_to_live = 2592000  -- auto-expire rows after 30 days (optional)
  AND comment = 'Real-time weather readings streamed from OpenWeather API via Kafka';


-- ── Useful queries to run in cqlsh ────────────────────────────────────────────

-- Latest 10 readings for Nairobi:
-- SELECT * FROM weather_records WHERE city = 'Nairobi' LIMIT 10;

-- All readings in a time window:
-- SELECT * FROM weather_records
--     WHERE city = 'Nairobi'
--       AND timestamp >= '2024-06-01 00:00:00'
--       AND timestamp <  '2024-06-02 00:00:00';

-- Count total records per city (requires ALLOW FILTERING on small datasets):
-- SELECT city, COUNT(*) FROM weather_records GROUP BY city;
