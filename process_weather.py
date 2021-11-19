import os
import time
import json
import requests
from ratelimit import limits, sleep_and_retry

API_KEY = os.getenv("API_KEY", "")
API_URL = "http://api.openweathermap.org/data/2.5/weather"
API_UNIT = os.getenv("API_UNIT", "metric")
MAX_CALLS = 60
PERIOD = 65

class ProcessWeather():
    def __init__(self, process_queue: object, progress: dict) -> None:
        self._process_queue = process_queue
        self._progress = progress

    @sleep_and_retry
    @limits(calls=MAX_CALLS, period=PERIOD)
    def _get_weather(self, city_id: int) -> dict:
        payload = {"id": city_id, "appid": API_KEY, "units": API_UNIT}
        response = requests.get(API_URL, params=payload)
        return response.json()

    def _parse_response(self, response: dict) -> dict:
        if response["cod"] == 200:
            return {
                "city_id": response["id"],
                "name": response["name"],
                "temp": response["main"]["temp"],
                "humidity": response["main"]["humidity"]
            }
        return response

    def _get_cities(self) -> list:
        with open("cities.csv", "r") as _file:
            return _file.read().splitlines()

    def _save_weather(self, request_id: int, responses: list) -> None:
        with open(f"{request_id}_weather_data.json", "w") as outfile:
            json.dump(responses, outfile)

    def _process(self, cities: list) -> None:
        total_cities = len(cities)
        if (not self._process_queue.empty()):
            request_id = self._process_queue.get()
            responses = []
            for i, city in enumerate(cities):
                response = self._parse_response(self._get_weather(city))
                responses.append(response)
                self._progress[request_id] = (i + 1) / total_cities
            self._save_weather(request_id, responses)
        else:
            time.sleep(1)

    def run(self) -> None:
        cities = self._get_cities()
        while (True):
            try:
                self._process(cities)
            except Exception as ex:
                print(f"Thread error: {ex}")
                time.sleep(0.10)
