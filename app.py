from flask import Flask, request, jsonify
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Weather Dashboard Backend is running"
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Backend is healthy"
    })


@app.route("/api/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({
            "status": "error",
            "message": "City name is required"
        }), 400

    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        geo_data = geo_response.json()

        if "results" not in geo_data or len(geo_data["results"]) == 0:
            return jsonify({
                "status": "error",
                "message": "City not found"
            }), 404

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")
        timezone = location.get("timezone", "")

        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,pressure_msl,wind_speed_10m,wind_direction_10m",
            "timezone": "auto"
        }

        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        weather_data = weather_response.json()

        current = weather_data.get("current", {})
        units = weather_data.get("current_units", {})

        weather_code = current.get("weather_code")
        condition = WEATHER_CODES.get(weather_code, "Unknown condition")

        return jsonify({
            "status": "success",
            "location": {
                "city": city_name,
                "country": country,
                "timezone": timezone,
                "latitude": latitude,
                "longitude": longitude
            },
            "weather": {
                "temperature": current.get("temperature_2m"),
                "temperature_unit": units.get("temperature_2m"),
                "feels_like": current.get("apparent_temperature"),
                "humidity": current.get("relative_humidity_2m"),
                "humidity_unit": units.get("relative_humidity_2m"),
                "precipitation": current.get("precipitation"),
                "cloud_cover": current.get("cloud_cover"),
                "pressure": current.get("pressure_msl"),
                "wind_speed": current.get("wind_speed_10m"),
                "wind_direction": current.get("wind_direction_10m"),
                "condition": condition,
                "weather_code": weather_code,
                "time": current.get("time")
            }
        })

    except requests.exceptions.RequestException:
        return jsonify({
            "status": "error",
            "message": "Weather service is not reachable"
        }), 500

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)