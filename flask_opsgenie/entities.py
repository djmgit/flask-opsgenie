from enum import Enum
from typing import Dict
from flask_opsgenie.exceptions import InvalidOpsgenieAlertParams

class AlertType(Enum):

    STATUS_ALERT = 1
    LATENCY_ALERT = 2
    EXCEPTION = 3


class AlertPriority(Enum):

    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"


class OpsgenieAlertParams:

    def __init__(self, opsgenie_token:str=None, alert_tags:Dict[str, str]=None, alert_alias:str=None,
                 alert_priority:str=None, alert_responder:Dict[str, str]=None, opsgenie_api_base:str=None,
                 ):
        self.opsgenie_token = opsgenie_token,
        if not self.opsgenie_token:
            raise InvalidOpsgenieAlertParams(f'Missing opsgenie api token')
        self.alert_tags = alert_tags

        # set default service id if not present
        if not alert_tags.get("service_id"):
            alert_tags["service_id"] = f'flask-service-{self.alert_tags["host"]}'
        self.alert_alias = alert_alias
        self.alert_priority = AlertPriority(alert_priority)
        self.alert_responder = alert_responder
        self.opsgenie_api_base = opsgenie_api_base
