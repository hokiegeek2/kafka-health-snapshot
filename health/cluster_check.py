#!/bin/python3

import json
from health import broker_check, topic_check

def getClusterStatus():
    broker_status = broker_check.getBrokerStatus()
    topics_status = topic_check.getTopicsStatus()
    
    if _statusGreen(broker_status) and _statusGreen(topics_status):
        return _getClusterGreenStatus()
    elif _statusRed(broker_status) or _statusRed(topics_status):
        return _getClusterRedStatus(broker_status, topics_status)
    else:
        return _getClusterYellowStatus(broker_status, topics_status)

def _getClusterGreenStatus():
    return '{"status": "green"}'

def _getClusterYellowStatus(broker_status, topics_status):
    cluster_reasons = _getCompositeStatusReasons(broker_status, topics_status)
    return '{"status": "yellow","reasons": ' + str(cluster_reasons) + '}'

def _getCompositeStatusReasons(broker_status, topics_status):
    b_status = json.loads(broker_status)
    t_status = json.loads(topics_status)
    
    composite_reasons = []
    if 'reasons' in b_status:
        composite_reasons += b_status['reasons']
    if 'reasons' in t_status:
        composite_reasons += t_status['reasons']
    return json.dumps(composite_reasons)

def _getClusterRedStatus(broker_status, topics_status):
    cluster_reasons = _getCompositeStatusReasons(broker_status, topics_status)
    return '{"status": "red","reasons": ' + str(cluster_reasons) + '}'

def _statusRed(status_json):
    status = json.loads(status_json)
    return status['status'] == 'red'

def _statusGreen(status_json):
    status = json.loads(status_json)
    return status['status'] == 'green'
