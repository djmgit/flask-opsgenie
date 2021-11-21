from typing import Dict, Optional
from flask import request
from flask_opsgenie.entities import AlertType, OpsgenieAlertParams

def raise_opsgenie_status_alert(alert_status_code:Optional[str] = None, alert_status_class:Optional[str] = None,
                                opsgenie_alert_params:OpsgenieAlertParams=None):
    pass


def raise_opsgenie_latency_alert(elapsed_time:int, opsgenie_alert_params:OpsgenieAlertParams=None):
    pass

def raise_opsgenie_alert(alert_type:AlertType = None, alert_status_code:Optional[int] = None, \
                         alert_status_class:Optional[str] = None, elapsed_time:Optional[int] = None,
                         opsgenie_alert_params:OpsgenieAlertParams=None):

    endpoint = request.path
    url = request.url
    method = request.method

    if alert_type == AlertType.STATUS_ALERT:
        if alert_status_code:
            raise_opsgenie_status_alert(alert_status_code=alert_status_code, opsgenie_alert_params=opsgenie_alert_params)
        elif alert_status_class:
            raise_opsgenie_status_alert(alert_status_class=alert_status_class, opsgenie_alert_params=opsgenie_alert_params)

    if alert_type == AlertType.LATENCY_ALERT:
        raise_opsgenie_alert(elapsed_time=elapsed_time, opsgenie_alert_params=opsgenie_alert_params)
