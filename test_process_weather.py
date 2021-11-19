import os
import pytest
from process_weather import ProcessWeather
from multiprocessing import Queue


@pytest.fixture(scope="module")
def get_process_weather():
    app_queue = Queue()
    app_queue.put(1)
    yield ProcessWeather(app_queue, {})

def test_get_cities_not_empty(get_process_weather):
    """
    GIVEN a ProcessWeather instance
    WHEN get_cities is called
    THEN check that the result is not empty
    """
    assert get_process_weather._get_cities() != []

def test_save_weather(get_process_weather):
    """
    GIVEN a ProcessWeather instance
    WHEN save_weather is called
    THEN check that the json file was saved
    """
    get_process_weather._save_weather(1, [{"test": 1}, {"test": 2}])
    with open(f"1_weather_data.json", "r") as _file:
        assert _file.read() == '[{"test": 1}, {"test": 2}]'
    os.remove("1_weather_data.json")

def test_parse_response_code_201(get_process_weather):
    """
    GIVEN a ProcessWeather instance
    WHEN parse_response is called with a parameter code 201
    THEN check that the result is equal to the sended parameter
    """
    assert get_process_weather._parse_response({"cod": 201}) == {"cod": 201}

def test_parse_response_code_200(get_process_weather):
    """
    GIVEN a ProcessWeather instance
    WHEN parse_response is called with json parameter with code 200
    THEN check that the result is in the expected format
    """
    response = {
        "cod": 200,
        "id": 1,
        "name": "London",
        "main": {
            "temp": 10,
            "humidity": 10
        }
    }
    result = {
        "city_id": 1,
        "name": "London",
        "temp": 10,
        "humidity": 10
    }
    assert get_process_weather._parse_response(response) == result

def test_get_weather(get_process_weather):
    """
    GIVEN a ProcessWeather instance
    WHEN get_weather is called with the city id 3439525
    THEN check that the result is the Young City
    """
    weather_data = get_process_weather._get_weather(3439525)
    assert weather_data["cod"] == 200
    assert weather_data["id"] == 3439525
    assert weather_data["name"] == "Young"

def test_process(get_process_weather):
    """
    GIVEN a ProcessWeather instance
    WHEN process is called with the cities list
    THEN check that the result is the Young City
    """
    get_process_weather._process([3439525])
    with open(f"1_weather_data.json", "r") as _file:
        assert '"city_id": 3439525' in _file.read()
    os.remove("1_weather_data.json")

def test_process_with_empty_queue(get_process_weather):
    """
    GIVEN a ProcessWeather instance
    WHEN process is called with an empty queue
    THEN check that nothing happens
    """
    get_process_weather._process([3439525])