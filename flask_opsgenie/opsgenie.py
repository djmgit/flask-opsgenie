from typing import Optional
from flask import request
from flask_opsgenie.entities import AlertType

def raise_opsgenie_alert(alert_type:AlertType, alert_status_code:Optional[int], alert_status_class:Optional[str]) -> None:
    pass
