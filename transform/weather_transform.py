from datetime import datetime


def transform_weather_data(raw_data):
    transformed = []
    for day in raw_data:
        try:
            transformed.append({
                "date": datetime.strptime(day["date"], "%m/%d/%Y"),
                "day_name": day["day"],
                "status": day["status"],
                "description": day["description"],
                "icon": day["icon"],
                "temp_day": float(day["degree"]),
                "temp_min": float(day["min"]),
                "temp_max": float(day["max"]),
                "temp_night": float(day["night"]),
                "humidity": float(day["humidity"])
            })
        except Exception as e:
            print(f"Error transforming day {day}: {e}")
    return transformed
