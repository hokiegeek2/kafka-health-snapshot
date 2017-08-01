#!/bin/python3

import json
from utils import os_utils,http_utils

def _allBrokersHealthy(expected_brokers, current_brokers):
    return not _getOfflineBrokers(expected_brokers, current_brokers)

def getBrokerStatus():
    expected_brokers = _getExpectedBrokers()
    current_brokers  = _getCurrentBrokers()
    
    if _allBrokersHealthy(expected_brokers,current_brokers):
        return '{"status": "green"}'
    elif not current_brokers:
        return '{"status": "red", "reasons": ["all brokers offline"]}'
    else:
        return '{"status":"yellow","reasons": ["brokers offline: ' + str(_getOfflineBrokers(expected_brokers, current_brokers)) + '"]}'

def _getOfflineBrokers(expected_brokers, current_brokers):
    return set(expected_brokers) - set(current_brokers)

def _getExpectedBrokers():
    return json.loads(os_utils.getEnvVariable('KAFKA_BROKERS', True))['brokers']

def _getCurrentBrokers():
    return http_utils.getJson('/brokers')['brokers']

