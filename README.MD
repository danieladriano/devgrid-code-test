# DevGrid - Open Weather

The API was built using **[Python](https://www.python.org/)** 3.8 and **[Flask](https://flask.palletsprojects.com/en/2.0.x/)** exposing two endpoints (`POST`, `GET`).

The `POST` receive a integer pathparam `ID` and adds into a queue. A thread consumes the queue and get the weather data from **[Open Weather](https://openweathermap.org/api)**. Due to an Open Weather limitation, only 60 cities per minute can be requested. To get the percentage of the `POST` progress `ID`, a `GET` endpoint can be requested with a pathparam `ID`.

The requests `IDs` are unique and can be used only once.

### Tools and frameworks

* **[Flask](https://flask.palletsprojects.com/en/2.0.x/)**: chosen due to its extensive documentation, wide usage in the market, and simplicity vs robustness;
* **[ratelimit](https://pypi.org/project/ratelimit/)**: used to control the amount of requests made to **[Open Weather](https://openweathermap.org/api)**;
* **[requests](https://docs.python-requests.org/en/latest/)**: used to make the requests in **[Open Weather](https://openweathermap.org/api)**;
* **[gunicorn](https://gunicorn.org/)**: a Python WSGI HTTP Server, compatible with various web frameworks and simply implemented. Used to serve the Flask application.


### Returned messages

1. `POST` - Starting weather search!
   
   `{"code": 202, "message": "Starting weather search!"}`

2. `POST` - Request already registered!
   
    `{"code": 200, "message": "Request already registered!"}`

3. `GET` - Request not found!

    `{"code": 401, "message": "Request not found!"}`

4. `GET` - Progress percentage

    `{"code": 200, "request": <request-id>, "progress": <progress>}`

### How to test

For testing, **[pytest](https://docs.pytest.org/en/6.2.x/)** and **[pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)** was used. To run:

`export API_KEY=<api-key>`
`pip install -r requirements.txt`
`pip install -r requirements-test.txt`
`pytest --cov -v`

### How to run - Local

To run:

`export API_KEY=<api-key>`
`pip install -r requirements.txt`
`python app.py`

### How to run - Docker

Before build the docker image, it's necessary to edit the `ENV API_KEY` in `Dockerfile` and put yours API Key.

Build image:

1. Build docker image
    `docker build --tag <image-name> .`
2. Run docker image
   `docker run --name <container-name> -d -it -p 8888:8888 <image-name>`

### How to use - Postman

Import `devgrid-code-test.postman_collection.json` file to use the API with Postman.
A variable `request_id` can be edit at `devgrid-code-test\variables`.