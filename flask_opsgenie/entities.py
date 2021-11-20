from enum import Enum

class AlertType(Enum):

    STATUS_ALERT = 1
    LATENCY_ALERT = 2


class OpsgenieAlertParams:

    def __init__(self, )