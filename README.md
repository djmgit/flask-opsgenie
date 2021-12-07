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
    SERVICE_ID = "my_flask_service"
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
    ALERT_TAGS = ["flask_latency_alert"]
    ALERT_PRIORITY = "P3"
    SERVICE_ID = "my_flask_service"
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

Above is the alert generated by flask-opsgenie for this example. Again, we have the same amount of details as before and a different alias this time to denote
its an latency related alert. Also, we do notice that now we have two new config parameters. First is ```THRESHOLD_RESPONSE_TIME``` which takes latency
time threshold in ms and then we have ```RESPONSE_TIME_MONITORED_ENDPOINTS``` which takes a list of regexes to match against a route path. If the route matches
with any of the regexes present in the list, that route path will be monitored and an alert will be generated if it breaches the response latency,

Finally, we can also generate alert when a route throws an exception for some reason. It might seem that we dont need to capture this situation since if a route
raises an exception, the response returned will be 500/5XX and hence we can have an alert for that. However that is always not true with flask. If we use
multiple ```@app.after_request``` decorated methods and if somehow one of those methods fail to return the respnse object at the end, the response (status 5XX)
will not be sent back to the user. In such scenario this config option provided by flask-opsgenie can help us.
Also the generated alert will have the exception in the alert body which can come quite handy for the on-call engineer.

So now lets see one finall example for this configuration.

```
class FlaskOpsgenieConfig:

    OPSGENIE_TOKEN = os.getenv("API_KEY")
    ALERT_TAGS = ["flask_exception_alert"]
    ALERT_PRIORITY = "P3"
    SERVICE_ID = "my_flask_service"
    ALERT_EXCEPTION = True
    RESPONDER = [{
        "type": "user",
        "username": "neo@matrix"
    }]

app = Flask(__name__)
app.config.from_object(FlaskOpsgenieConfig())
flask_opsgenie = FlaskOpsgenie(None)
flask_opsgenie.init_app(app)

@app.route("/res_ex", methods=["GET"])
def res_ex():
    a = 1/0
    return "I am assuming everything is fine, but there might be exception", 200

```

If we hit ```/res_ex```, flask_opsgenie will raise an alert since this route will be throwing a Division by Zero exception.

![Screenshot 2021-12-05 at 5 44 31 PM](https://user-images.githubusercontent.com/16368427/144746096-49f3c6a4-aa25-4507-8c0a-798747b16ab9.png)

For switching on exception monitoring all we need to do is add ```ALERT_EXCEPTION = True``` to our config.

## Flask-opsgenie configuration in details

As already shown in the quick start guide, initialising flask-opsgenie is pretty easy just like any other flask extention. We can either pass the flask app
object to the FlaskOpsgenie constructor or use the the init method of initialising flask-opsgenie. We can load the config as an object or from a config file.

In this section we will go through all the different config option that flask-opsgenie provides, how we can use them and what default values they assume.

### Config options provided by flask-opsgenie

- **ALERT_STATUS_CODES** : This takes a list of status codes. Our flask service endpoints will be monitored against these response status codes. By default all
the endpoints/routes will be monitored, but this can be controlled, as mentioned below.

- **ALERT_STATUS_CLASS** : This takes a list of response status classes like ```5XX, 4XX or 3XX` etc. For example if the provided value is ```["5XX", "4XX"]```
any request throwing a 501 or 502 or 404 or 403 etc will raise opsgenie alert. Again by default if this param is present, all the route response status codes
will be monitored, however this too can be controlled. If both ```ALERT_STATUS_CODES``` and ```ALERT_STATUS_CLASS``` are provided, then ```ALERT_STATUS_CODES```
will be given priority. That is if we are monitoring for both 501 and 5XX, there will be only one alert generated and not two.

- **MONITORED_ENDPOINTS** : This takes in a list of regexes. With this we can limit the endpoints that will be monitored for or whose response status code/class
will be matched against the provided params. The request endpoints will be matched against the given list of regexes and only the matching paths will be
evaluated against the given rules. It is to be noted that the given regex should be provided keeping only the request/route path in mind, niether the complete
url nor the query params.


