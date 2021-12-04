# Flask Opsgenie

Flask-opsgenie is a flask extension for creating alerts on Opsgenie. Once configured flask-opsgenie can generate an opsgenie alert once a desired condition is met,
for example an endpoint returns an unwanted status code (500 may be) or an unwanted status class (5XX or 3XX for some reason) or lets say a given endpoint is
breaching response latency threshold or may be it has thrown some exception. Flask-opsgenie will try to send as much details as possible to Opsgenie so that
the on-call rockstar can get most of the details looking at the phone screen on receiving the page.

## Getting flask-opsgenie

Flask-opsgenie is not yet present on PyPI. To install flask-opsgenie you will have to install it from source, which is this repository

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
response status code and the given endpoint returns the same. If we want we can provide several status codes to be monitored like :
``` ALERT_STATUS_CODES = [500, 501, 502] ```
This will generate an alert if any of the mentioned status codes is returned. So if you want to monitor for all the 5's status codes you can keep on mentioning
all of them like ``` 500, 501, 502, 503 ...` or even better you can use ``` ALERT_STATUS_CLASSES = ["5XX"] ``` instead of ```` ALERT_STATUS_CODES ```. As the
name suggests ``` ALERT_STATUS_CLASSES ``` instructs flask-opsgenie to monitor for entire classes of status codes which in this case will be the ``` 5XX ``` class
which means 500, 501, 502 and so on till 510. Isn't that cool?

