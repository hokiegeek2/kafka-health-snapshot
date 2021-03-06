#!/usr/bin/python3

import os,json,time
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
from utils import http_utils, os_utils
from health import cluster_check, topic_check

bhost = socket.gethostname()
ip = ip = ([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])



"""Host and Port for python web server, HOST_NAME can be represented by
either the FQDN or plain old IP address.
"""
HOST_NAME = str(ip)
PORT_NUMBER = 8000

# pass/fail params
FAIL_LOADAVG=4

class HealthCheckServer(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        response_json = s._getResponseJson(s.path)
        response_code = s._getResponseCode(response_json)

        s.send_response(response_code)
        s.send_header("Content-type", "application/json")
        s.end_headers()
        s.wfile.write(bytes(response_json, 'utf-8'))

    def _getResponseJson(self,path):
        if path == '/cluster/health':
            return cluster_check.getClusterStatus()
        elif path.startswith('/topic/health/'):
            topic = path.split('/topic/health/')[1]
            if not topic:
                return '{"error": "You must specify the topic in the form of /topic/health/<topic name"}'
            return topic_check.getTopicStatus(topic)
        elif path == '/ruok':
            return '{"status": "imok"}'
        else:
            return '{"error": "invalid request, check path ' + path + '"}'

    def _getResponseCode(self,status_json):
        if 'status' not in status_json:
            return 404
        elif self._clusterStatusHealthy(status_json):
            return 200
        elif self._imOk(status_json):
            return 200
        else:
            return 500
       
    def _clusterStatusHealthy(self,status):
        cluster_status = json.loads(status)['status']
        if cluster_status == "green" or cluster_status == "yellow":
            return True
        else:
            return False
    def _imOk(self,status_json):
        if json.loads(status_json)['status'] == 'imok':
            return True

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), HealthCheckServer)
    print("Starting Kafka Health Checker - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Stopping Kafka Health Checker - %s:%s" % (HOST_NAME, PORT_NUMBER))

