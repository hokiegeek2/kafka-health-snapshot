#!/bin/python3

import requests,json
from utils import os_utils

def getHealthUrl(path):
    rest_url = os_utils.getEnvVariable('KAFKA_REST_URL',True)
    return rest_url + path

def getJson(path):
    return requests.get(getHealthUrl(path)).json()
