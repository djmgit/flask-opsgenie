from enum import Enum
from typing import Dict
from flask_opsgenie.exceptions import InvalidOpsgenieAlertParams

class AlertType(Enum):

    STATUS_ALERT = 1
    LATENCY_ALERT = 2


class OpsgenieAlertParams:

    def __init__(self, opsgenie_token:str=None, alert_tags:Dict[str, str]=None, alert_alias:str=None,
                 alert_priority:str=None, alert_responder:Dict[str, str]=None, opsgenie_api_base:str=None,
                 ):
        self.opsgenie_token = opsgenie_token,
        if not self.opsgenie_token:
            raise InvalidOpsgenieAlertParams(f'Missing opsgenie api token')
        self.alert_tags = alert_tags
        self.alert_alias = alert_alias
        self.alert_priority = alert_priority
        self.alert_responder = alert_responder
        self.opsgenie_api_base = opsgenie_api_base
