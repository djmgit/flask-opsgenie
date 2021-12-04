# Flask Opsgenie

Flask-opsgenie is a flask extension for creating alerts on Opsgenie. Once configured flask-opsgenie can generate an opsgenie alert once a desired condition is met,
for example an endpoint returns an unwanted status code (500 may be) or an unwanted status class (5XX or 3XX for some reason) or lets say a given endpoint is
breaching response latency threshold or may be it has thrown some exception. Flask-opsgenie will try to send as much details as possible to Opsgenie so that
the on-call rockstar can get most of the details looking at the phone screen on receiving the page.
