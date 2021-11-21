from typing import Dict, Optional
from flask import request
from flask_opsgenie.entities import AlertType, OpsgenieAlertParams

def raise_opsgenie_alert(alert_type:AlertType = None, alert_status_code:Optional[int] = None, \
                         alert_status_class:Optional[str] = None, elapsed_time:Optional[int] = None,
                         opsgenie_alert_params:OpsgenieAlertParams=None) -> None:

    endpoint = request.path
    url = request.url
    method = request.method
