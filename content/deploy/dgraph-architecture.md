+++
title = "Dgraph Architecture"
type = "docs"
description = "Learn about Dgraph's distributed architecture, cluster components, scaling strategies, and how it achieves high performance and availability for graph databases."
[menu.main]
    name = "Architecture"
    identifier = "architecture"
    parent = "deploy"
    weight = 1
+++

Dgraph is designed from the ground up as a distributed graph database, enabling it to scale to larger data sizes and higher throughput than traditional single-node graph databases. The architecture consists of multiple server nodes that work together to form a single logical data store, providing both horizontal scalability and high availability.

## Cluster Components

A Dgraph cluster consists of two main types of nodes, each serving specific functions:

#### Dgraph Zero (Management Nodes)
Dgraph Zero nodes are the control plane of the cluster, responsible for:

- **Cluster Coordination**: Managing the overall cluster state and node membership
- **Metadata Storage**: Maintaining information about data distribution and cluster topology
- **Transaction Coordination**: Orchestrating distributed transactions across multiple Alpha nodes
- **Data Rebalancing**: Automatically moving data between Alpha nodes to maintain optimal distribution
- **Schema Management**: Coordinating schema changes across the cluster
- **Backup Coordination**: Managing backup and restore operations
#### Dgraph Alpha (Data Nodes)
Dgraph Alpha nodes are the data plane of the cluster, responsible for:

- **Data Storage**: Storing the actual graph data (nodes, edges, and attributes)
- **Index Management**: Maintaining various indexes for efficient querying
- **Query Processing**: Executing queries and mutations on the stored data
- **Predicate Storage**: Organizing data by predicates (relationship types) for optimal performance
- **Transaction Processing**: Handling ACID transactions for data consistency

{{<figure class="medium image" src="/images/overview/dgraph-architecture.png" title="Dgraph Internal Architecture" alt="Architecture of Dgraph showing Zero and Alpha nodes">}}

## Distributed Design Benefits

Dgraph's distributed architecture provides several key advantages:

### Horizontal Scalability
- **Add Nodes**: Scale by adding more Alpha nodes to handle increased data volume
- **Linear Performance**: Query performance scales linearly with the number of nodes
- **Load Distribution**: Workload is automatically distributed across available nodes

### High Availability
- **Fault Tolerance**: Cluster continues operating even when individual nodes fail
- **Automatic Failover**: Seamless transition when nodes become unavailable
- **Data Redundancy**: Multiple copies of data ensure no data loss

### Query Performance
- **N-Hop Queries**: Queries with depth N require only N network hops, regardless of data size
- **Parallel Processing**: Queries are executed in parallel across relevant nodes
- **Predicate-Based Sharding**: Data is organized by predicates for optimal query performance

## Scaling Strategies

### Minimum Configuration
Every Dgraph cluster requires at least:
- **1 Dgraph Zero node**: For cluster coordination
- **1 Dgraph Alpha node**: For data storage and querying

This minimal setup is suitable for development and testing environments.

### High Availability Configuration
For production environments, Dgraph recommends:

- **3 Dgraph Zero nodes**: Provides fault tolerance for cluster coordination
- **3 Dgraph Alpha nodes**: Ensures data availability and query performance

This configuration provides:
- **Automatic Failover**: If one node fails, the cluster continues operating
- **Data Redundancy**: Each piece of data is replicated across multiple nodes
- **Load Distribution**: Queries are distributed across all available nodes

### Large-Scale Sharding
For datasets exceeding 1TB or requiring maximum performance:

- **Multiple Server Groups**: Data is sharded across multiple groups of Alpha nodes
- **Predicate-Based Distribution**: Each predicate (relationship type) is assigned to specific server groups
- **Cross-Group Queries**: Queries spanning multiple predicates are automatically coordinated across groups

## Data Organization

### Predicate-Based Storage
Unlike traditional graph databases, Dgraph organizes data by predicates (relationship types) rather than by nodes. This approach provides:

- **Efficient Indexing**: Each predicate has its own optimized indexes
- **Parallel Processing**: Queries can be executed in parallel across predicate shards
- **Scalable Updates**: Mutations affect only the relevant predicate shards

### Index Management
Dgraph maintains various types of indexes for different query patterns:

- **Token Indexes**: For exact matches and range queries
- **Reverse Indexes**: For bidirectional relationship traversal
- **Full-Text Indexes**: For text search capabilities
- **Geographic Indexes**: For location-based queries
- **Custom Indexes**: For specialized query requirements

## Cluster Management

### Automatic Operations
Dgraph handles many operational tasks automatically:

- **Data Rebalancing**: Automatically moves data to maintain optimal distribution
- **Node Recovery**: Detects and recovers from node failures
- **Load Balancing**: Distributes queries across available nodes
- **Schema Propagation**: Ensures schema changes are applied consistently

### Monitoring and Observability
Built-in monitoring capabilities include:

- **Health Checks**: Continuous monitoring of node and cluster health
- **Performance Metrics**: Query latency, throughput, and resource utilization
- **Cluster Topology**: Real-time view of cluster structure and data distribution
- **Alert Integration**: Integration with monitoring systems like Prometheus and Grafana

## Deployment Considerations

### Resource Requirements
- **CPU**: Multi-core processors recommended for optimal performance
- **Memory**: Sufficient RAM for caching and query processing
- **Storage**: Fast SSD storage for data persistence and indexes
- **Network**: Low-latency network connections between nodes

### Security
- **Encryption**: Support for encryption at rest and in transit
- **Access Control**: Fine-grained permissions for cluster management
- **Network Security**: Secure communication between cluster nodes
- **Audit Logging**: Comprehensive logging of cluster operations

## What's Next

- Learn about [cluster setup]({{< relref "cluster-setup" >}}) and configuration
- Explore [deployment options]({{< relref "installation" >}}) for different environments
- Understand [monitoring and maintenance]({{< relref "monitoring" >}}) best practices
- Review the [production checklist]({{< relref "cluster-checklist" >}}) for deployment
