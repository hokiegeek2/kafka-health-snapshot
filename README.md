# kafka-health-snapshot

Provides a REST API for checking the status of a Kafka cluster. REST endpoints provided for cluster as well as topic and broker-level statuses. kafka-health-snapshot is written in Python and uses REST calls to determine the status of the cluster, the brokers, or 1..n topics

# Status Designations
1. green--all brokers up, no under-replicated topic partitions
2. yellow--one or more brokers down and/or one or more under-replicated partitions (one or more replicas out of sync)
3. red--all brokers down and/or one or more out-of-sync leader replicas, the latter meaning that one or more topics cannot be written to or read from.

# REST Endpoints
/cluster/health -- provides high-level status of cluster
/topic/health/<topic name>--provides health status of a topic

# Dependencies
kafka-health-snapshot is dependent upon the kafka-rest REST API for Kafka. The kafka-rest server can either be deployed with kafka-health-snapshot or independently.

# Environment Variables
1. KAFKA_REST_URL='http://hsot:port of kafka-rest server'
2. KAFKA_BROKERS='{"brokers": [<broker list form kafka-rest>]}'
