#!/bin/python3

import json
from utils import http_utils

healthy_status = '{"status": "green"}'

def topicsHealthy():
    topics = _getTopics()
 
    topics_not_in_sync = []

    for topic in topics: 
        if topicReplicasInSync(topic) == False:
            return False
    return True

def getTopicsStatus():
    topics = _getTopics()
    out_of_sync_leaders = []
    out_of_sync_followers = []
    for topic in topics:
        oos_topic_replicas = _getOutOfSyncTopicReplicas(topic)
        if oos_topic_replicas:
            leader = oos_topic_replicas['leader']
            followers = oos_topic_replicas['followers']
            if leader:
                out_of_synch_leaders.extend(leader)
            if followers:
                out_of_sync_followers.extend(followers)

    if out_of_sync_leaders:
        return '{"status": "red", "reasons": "out of sync leaders ' + json.dump(out_of_sync_leaders) + '}'
    elif out_of_sync_followers:
        return '{"status": "yellow", "reasons": "out of sync followers ' + json.dump(out_of_sync_followers) + '}'
    else:
        return '{"status": "green"}'

def topicReplicasInSync(topic):
    partitions = _getPartitions(topic)
    for partition in partitions:
        if _partitionReplicasInSync(partition) == False:
            return False
    return True

def _getOutOfSyncTopicReplicas(topic):
    partitions = _getPartitions(topic)
    

def _getOutOfSyncReplicas(partition):
    out_of_sync = {}
    out_of_sync_followers = []
    replicas = partition['replicas']

    for replica in replicas:
        print(str(replica['broker']) + str(replica['leader']) + str(replica['in_sync']))
        if replica['in_sync'] == True:
            if replica['leader']:
                out_of_sync['leader'] = replica
            else:
                out_of_sync_followers += replica

    if out_of_sync_followers:
        out_of_sync['followers'] = out_of_sync_followers
    return out_of_sync

def _partitionReplicasInSync(partition):
    replicas = partition['replicas']
    for replica in replicas:
        print(str(replica['broker']) + str(replica['leader']) + str(replica['in_sync']))
        if replica['in_sync'] == False:
            return False
    return True

def _getPartitions(topic):
    return http_utils.getJson('/topics/' + topic + '/partitions')

def _getTopics():
    return http_utils.getJson('/topics')
