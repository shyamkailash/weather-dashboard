import unittest
from unittest.mock import patch

from app import app


class WeatherApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("app.requests.get")
    def test_weather_response_includes_requested_area_and_place(self, mock_get):
        class MockResponse:
            def __init__(self, payload):
                self._payload = payload

            def json(self):
                return self._payload

        mock_get.side_effect = [
            MockResponse({
                "results": [{
                    "name": "Coimbatore",
                    "country": "India",
                    "latitude": 11.0,
                    "longitude": 76.0,
                    "timezone": "Asia/Kolkata"
                }]
            }),
            MockResponse({
                "current": {
                    "temperature_2m": 30.5,
                    "relative_humidity_2m": 50,
                    "apparent_temperature": 32.0,
                    "precipitation": 0.0,
                    "weather_code": 0,
                    "cloud_cover": 20,
                    "pressure_msl": 1000.0,
                    "wind_speed_10m": 4.0,
                    "wind_direction_10m": 180,
                    "time": "2026-06-25T14:30"
                },
                "current_units": {
                    "temperature_2m": "°C",
                    "relative_humidity_2m": "%",
                    "apparent_temperature": "°C",
                    "precipitation": "mm",
                    "cloud_cover": "%",
                    "pressure_msl": "hPa",
                    "wind_speed_10m": "km/h",
                    "wind_direction_10m": "°",
                    "time": "iso8601"
                }
            })
        ]

        response = self.client.get("/api/weather?city=Coimbatore&area=Tamil%20Nadu&place=Coimbatore")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["user_request"]["area"], "Tamil Nadu")
        self.assertEqual(payload["user_request"]["place"], "Coimbatore")


if __name__ == "__main__":
    unittest.main()
