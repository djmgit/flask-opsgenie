# Flask Opsgenie

Flask-opsgenie is a flask extension for creating alerts on Opsgenie. Once configured flask-opsgenie can generate an opsgenie alert once a desired condition is met,
for example an endpoint returns an unwanted status code (500 may be) or an unwanted status class (5XX or 3XX for some reason) or lets say a given endpoint is
breaching response latency threshold or may be it has thrown some exception. Flask-opsgenie will try to send as much details as possible to Opsgenie so that
the on-call rockstar can get most of the details looking at the phone screen on receiving the page.

## Getting flask-opsgenie

Flask-opsgenie is not yet present on PyPI. To install flask-opsgenie we will have to install it from source, which is this repository

- Clone this repo using ``` git clone https://github.com/djmgit/flask-opsgenie.git ```
- ``` cd flask-opsgenie ```
- ``` python3 setup.py install ```

## Quick Start

Lets quickly see how to use flask-opsgenie in an actual flask application.
For an easy to get started with example, lets say we want to generate an opsgenie alert whenever a route returns 500 as response status code. Using
flask-opsgenie we do not need to write our own middleware code to generate the alert.

```
from flask import Flask
from flask_opsgenie import FlaskOpsgenie

class FlaskOpsgenieConfig:

    ALERT_STATUS_CODES = [500]
    OPSGENIE_TOKEN = os.getenv("API_KEY")
    ALERT_TAGS = ["flask_status_alert"]
    ALERT_PRIORITY = "P3"
    SERVICE_ID = "my_flask_service
    RESPONDER = [{
        "type": "user",
        "username": "neo@matrix"
    }]

app = Flask(__name__)
app.config.from_object(FlaskOpsgenieConfig())
flask_opsgenie = FlaskOpsgenie(None)
flask_opsgenie.init_app(app)

@app.route("/index", methods=["GET"])
def index():
    return "Hello world", 200

@app.route("/res500", methods=["GET"])
def res_500():
    return "This is a 500", 500
```

If we run this above tiny application and try to hit ``` /res500 ``` endpoint, it will generate an opsgenie alert because we are monitoring for ``` 500 ```
response status code and the given endpoint returns the same. 

![Screenshot 2021-12-05 at 4 54 55 PM](https://user-images.githubusercontent.com/16368427/144744662-8b638b1f-7237-4b86-bd24-c37808c495e8.png)

This is the alert we get out of the box using the bare minimum configuration we used above. As it can bee seen, flask-opsgenie decides for an appropriate alias
for this alert so that similar alerts can be grouped in future. It also provides several details in the details section like the path, method, url and response
of the request and additionaly the host which served the request. The alias can always be overriden as well.

If we want we can provide several status codes to be monitored like : ``` ALERT_STATUS_CODES = [500, 501, 502] ```
This will generate an alert if any of the mentioned status codes is returned. So if we want to monitor for all the 5's status codes we can keep on mentioning
all of them like ``` 500, 501, 502, 503 ...``` or even better we can use ``` ALERT_STATUS_CLASSES = ["5XX"] ``` instead of ``` ALERT_STATUS_CODES ```. As the
name suggests ``` ALERT_STATUS_CLASSES ``` instructs flask-opsgenie to monitor for entire classes of status codes which in this case will be the ``` 5XX ``` class
which means 500, 501, 502 and so on till 510. Isn't that cool?
We can also chose to monitor a given set of routes/endpoints, conversely we can chose to monitor all the endpoints for the response status code alert and decide
to ignore a few. More on that later.

We can also configure flask-opsgnie such that it generates an opsegenie alert when a monitored route breaches response time latency. Lets see an example for that.
For this example let us consider the following flask snippet.

```
import time

class FlaskOpsgenieConfig:

    OPSGENIE_TOKEN = os.getenv("API_KEY")
    ALERT_TAGS = ["flask_status_alert"]
    ALERT_PRIORITY = "P3"
    SERVICE_ID = "my_flask_service
    THRESHOLD_RESPONSE_TIME = 2000.0 # time is required in ms
    RESPONSE_TIME_MONITORED_ENDPOINTS = ["^\/res_slow\/\d+\/info\/$"]
    RESPONDER = [{
        "type": "user",
        "username": "neo@matrix"
    }]

app = Flask(__name__)
app.config.from_object(FlaskOpsgenieConfig())
flask_opsgenie = FlaskOpsgenie(None)
flask_opsgenie.init_app(app)

@app.route("/res_slow/<id_num>/info/", methods=["GET"])
def res_slow(id_num):
    time.sleep(3)
    return f'I am slow, {id_num}', 200
```

Once again, if we run this above tiny flask application and hit ```/res_slow/1/info/``` it will generate an opsgenie alert because the route takes more than
2s or 2000ms to return a response.

![Screenshot 2021-12-05 at 5 21 54 PM](https://user-images.githubusercontent.com/16368427/144745379-393d9389-7233-4b05-8939-3bfd62f689a3.png)


