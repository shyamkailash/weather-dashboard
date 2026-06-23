# Weather Dashboard Backend

A simple Flask backend for a Weather Dashboard application. It fetches current weather data using the Open-Meteo API.

## Features

- Search weather by city name
- Get temperature, humidity, wind speed, pressure, wind speed, and weather condition
- Flask REST API backend
- Uses Open-Meteo API
- Tested using curl in terminal

## Tech Stack

- Python
- Flask
- Flask-CORS
- Requests
- Open-Meteo API

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check backend status |
| GET | `/api/health` | Health check |
| GET | `/api/weather?city=CityName` | Get weather by city |

## How to Run

```bash
pip install -r requirements.txt
python app.py
Backend runs at: http://127.0.0.1:5000
Example
curl "http://127.0.0.1:5000/api/weather?city=Coimbatore"

Author
Shyam Kailash
EOF