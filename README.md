# kafka-health-snapshot
## Overview
Provides a REST API for getting a health snapshot of a Kafka cluster. REST endpoints provided for cluster as well as topic and broker-level statuses. kafka-health-snapshot is written in Python and uses REST calls to kafka-rest in order to determine the status of the cluster, the brokers, or 1..n topics

## Why Use kafka-health-snapshot
There are a few really good projects that provide kafka health checks. What's different about kafka-health-snapshot is that it is designed to provide a REST API that can be called on a user-specified schedule to provide snapshots of kafka cluster, broker, or topic health to service orchestration and monitoring frameworks such as Marathon and Consul. 

# Status Designations
1. green--all brokers up, no under-replicated topic partitions
2. yellow--one or more brokers down and/or one or more under-replicated partitions (one or more replicas out of sync)
3. red--all brokers down and/or one or more out-of-sync leader replicas, the latter meaning that one or more topics cannot be written to or read from.

# REST Endpoints
1. /cluster/health -- provides high-level status of cluster
2. /topic/health/<topic name>--provides health status of a topic
3. /ruok--health check for the kafka-health-snapshot REST server

# Dependencies
kafka-health-snapshot is dependent upon the kafka-rest REST API for Kafka, where kafka-health-snapshot delegates to kafka-rest to provide cluster, broker, and topic health snapshots The kafka-rest server can either be deployed with kafka-health-snapshot or independently.

# Environment Variables
1. KAFKA_REST_URL='http://host:port of kafka-rest server'
2. KAFKA_BROKERS='{"brokers": [brokerid1,brokerid2...]}'
