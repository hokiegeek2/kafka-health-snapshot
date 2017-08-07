#!/bin/python3

import json
from utils import http_utils

def getTopicsStatus():
    topics = _getTopics()
    out_of_sync_leaders = []
    out_of_sync_followers = []
    for topic in topics:
        oos_topic_replicas = _getOutOfSyncTopicReplicas(topic)
        if oos_topic_replicas:
            if 'leader' in oos_topic_replicas:
                leader = oos_topic_replicas['leader']
                out_of_synch_leaders.extend(leader)
            if 'followers' in oos_topic_replicas:
                followers = oos_topic_replicas['followers']
                out_of_sync_followers.extend(followers)

    if out_of_sync_leaders:
        return '{"status": "red", "reasons": ["out of sync leaders"]}'
    elif out_of_sync_followers:
        print(json.dumps(out_of_sync_followers))
        return '{"status": "yellow", "reasons": ["out of sync followers"]}'
    else:
        return '{"status": "green"}'

def getTopicStatus(topic):
   oos_topic_replicas = _getOutOfSyncTopicReplicas(topic)
   if oos_topic_replicas:
       if 'leader' in oos_topic_replicas:
           return '{"status": "red", "reason": "leader out of sync"}'
       elif 'followers' in oos_topic_replicas:
           followers = oos_topic_replicas['followers']
           return '{"status": "yellow", "reason": "out of sync followers ' + json.dumps(oos_topic_replicas) + '})'
   else:
       return '{"status": "green"}'

def _getOutOfSyncTopicReplicas(topic):
    partitions = _getPartitions(topic)
    out_of_sync = {}
    out_of_sync['followers'] = []
    for partition in partitions:
        oos = _getOutOfSyncReplicas(topic, partition)
        if 'followers' in oos:
            out_of_sync['followers'] +=  _getOutOfSyncReplicas(topic, partition)['followers'] 
    return out_of_sync   

def _getOutOfSyncReplicas(topic, partition):
    out_of_sync = {}
    out_of_sync_followers = []
    replicas = partition['replicas']
    for replica in replicas:
        if replica['in_sync'] == False:
            if replica['leader']:
                out_of_sync['leader'] = replica
            else:
                replica['partition'] = partition['partition']
                replica['topic'] = topic
                out_of_sync_followers.append(replica)

    if out_of_sync_followers:
        out_of_sync['followers'] = out_of_sync_followers
    return out_of_sync

def _getPartitions(topic):
    return http_utils.getJson('/topics/' + topic + '/partitions')

def _getTopics():
    return http_utils.getJson('/topics')
