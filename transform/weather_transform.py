from datetime import datetime
import pandas as pd


def transform_weather_data(raw_data):
    try:
        if not raw_data:
            return pd.DataFrame()

        df = pd.DataFrame(raw_data)

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        df["year"] = df["timestamp"].dt.year
        print(df["year"])
        df["month"] = df["timestamp"].dt.month_name()
        print(df["month"])

        df["day"] = df["timestamp"].dt.day
        print(df["day"])

        df["time"] = df["timestamp"].dt.time
        print(df["time"])

        df["weekday"] = df["timestamp"].dt.day_name()
        print(df["weekday"])

        numeric_cols = [
            "temperature",
            "feels_like",
            "humidity",
            "pressure",
            "wind_speed"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df[
            [
                "city",
                "country",
                "timestamp",
                "time",
                "day",
                "weekday",
                "month",
                "year",
                "temperature",
                "feels_like",
                "humidity",
                "pressure",
                "wind_speed",
                "weather",
                "description",
            ]
        ]

        return df

    except Exception as e:
        print(f"Transformation failed: {e}")
        return pd.DataFrame()
