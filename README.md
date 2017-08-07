# kafka-health-snapshot

Provides a REST API for checking the status of a Kafka cluster. REST endpoints provided for cluster as well as topic and broker-level status

# Status Designations
1. green--all brokers up, no under-replicated topic partitions
2. yellow--one or more brokers down and/or one or more under-replicated follower replicas
3. red--all brokers down and/or one or more under-replicated leader replicas

# REST Endpoints
/cluster/health -- provides high-level status of cluster
/topic/health/<topic name>--provides health status of a topic
