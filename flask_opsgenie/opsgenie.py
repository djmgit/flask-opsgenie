from typing import Dict, Optional
from flask import request
from flask_opsgenie.entities import AlertType

def raise_opsgenie_alert(alert_type:AlertType = None, alert_status_code:Optional[int] = None, \
        alert_status_class:Optional[str] = None, elapsed_time:Optional[int] = None, tags:Dict[str,str] = None) -> None:

    endpoint = request.path
    url = request.url
    method = request.method
