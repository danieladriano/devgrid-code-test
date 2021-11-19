import os
from flask import Flask, request
from multiprocessing import Process, Queue, Manager
from process_weather import ProcessWeather

app = Flask(__name__)

app_queue = Queue()
progress = Manager().dict()
Process(target=ProcessWeather(app_queue, progress).run).start()

PORT = os.getenv("PORT", 8888)
OK = 200
ACCEPTED = 202
UNAUTHORIZED = 401

def _weather_post(request_id: int) -> object:
    if request_id in progress:
        return {"code": OK, "message": "Request already registered!"}, OK

    progress[request_id] = 0.0
    app_queue.put(request_id)

    return {"code": ACCEPTED, "message": "Starting weather search!"}, ACCEPTED

def _weather_get(request_id: int) -> object:
    if request_id in progress:
        return {"code": OK, "request": request_id, "progress": f"{progress[request_id]:.2%}"}, OK
    return {"code": UNAUTHORIZED, "message": "Request not found!"}, UNAUTHORIZED

@app.route("/weather/<request_id>", methods=["GET", "POST"])
def weather(request_id):
    if request.method == "POST":
        return _weather_post(request_id)
    elif request.method == "GET":
        return _weather_get(request_id)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)
