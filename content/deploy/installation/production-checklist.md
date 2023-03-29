+++
date = "2017-03-20T22:25:17+11:00"
title = "Production checklist"
description = "Requirements to install Dgraph in a production environment"
weight = 2
[menu.main]
    parent = "installation"
+++

This guide describes important setup recommendations for a production-ready Dgraph cluster, ensuring high availability with external persistent storage, automatic recovery of failed services, automatic recovery of failed systems such as virtual machines, and disaster recovery such as backup/restore or export/import with automation.

{{% notice "note" %}}
In this guide, a node refers to a Dgraph instance unless specified otherwise.
{{% /notice %}}

A **Dgraph cluster** is comprised of multiple **Dgraph instances** or nodes connected together to form a single distributed database. A Dgraph instance is either a **Dgraph Zero** or **Dgraph Alpha**, each of which serves a different role in the cluster.

Once installed you may also install or use a **Dgraph client** to communicate with the database and perform queries, mutations, alter schema operations and so on. Pure HTTP calls from curl, Postman, or another program are also possible without a specific client, but there are a range of clients that provide higher-level language bindings, and which use optimized gRPC for communications to the database. Any standards-compliant GraphQL client will work with Dgraph to run GraphQL operations. To run DQL and other Dgraph-specific operations, use a Dgraph client.

Dgraph provides official clients for Go, Java, Python, and JavaScript, and C#, and the JavaScript client supports both gRPC and HTTP to run more easily in a browser. Community-developed Dgraph clients for other languages are also available. The full list of clients can be found in [Clients]({{< relref "clients" >}}) page. One particular client, Dgraph Ratel, is a more sophisticated UI tool used to visualize queries, run mutations, and manage schemas in both GraphQL and DQL. Note that clients are not part of a database cluster, and simply connect to one or more Dgraph Alpha instances.

### Cluster Requirements

A minimum of one Dgraph Zero and one Dgraph Alpha is needed for a working cluster.

There can be multiple Dgraph Zeros and Dgraph Alphas running in a single cluster.


### Machine Requirements

To ensure predictable performance characteristics, Dgraph instances should **not** run on "burstable" or throttled machines that limit resources. That includes t2 class machines on AWS.

To ensure that Dgraph is highly-available, we recommend each Dgraph instance be deployed to a different underlying host machine, and ideally that machines are in different availability zones or racks. In the event of an underlying machine failure, it is critical that only one Dgraph alpha and one Dgraph zero be offline so that 2 of the 3 instances in each group maintain a quorum. Also when using VMs or Docker/K8s, ensure machines are not over-subscribed and ideally not co-resident with other processes that will interrupt and delay Dgraph processing.

If you'd like to run Dgraph with fewer machines, then the recommended configuration is to run a single Dgraph Zero and a single Dgraph Alpha per machine. In a high availability setup, that allows the cluster to lose a single machine (simultaneously losing a Dgraph Zero and a Dgraph Alpha) with continued availability of the database.

Do not run multiple Dgraph Zeros or Dgraph Alpha processes on a single machine. This can affect performance due to shared resource issues and reduce availability in the event of machine failures.

### Operating System

Dgraph is designed to run on Linux. To run Dgraph on Windows
and macOS, use the [standalone Docker image]({{<relref "dgraph-overview#to-run-dgraph-using-the-standalone-docker-image">}}).

### CPU and Memory


We recommend 8 vCPUs or cores on each of three HA alpha instances for production loads, with 16 GiB+ memory per node.

You'll want a ensure that your CPU and memory resources are sufficient for your production workload. A common configuration for Dgraph is 16 CPUs and 32 GiB of memory per machine. Dgraph is designed with concurrency in mind, so more cores means quicker processing and higher throughput of requests.

You may find you'll need more CPU cores and memory for your specific use case.

### Disk

Dgraph instances make heavy use of disks, so storage with high IOPS is highly recommended to ensure reliable performance. Specifically SSDs, not HDDs.

Regarding disk IOPS, the recommendation is:
* 1000 IOPS minimum
* 3000 IOPS for medium and large datasets

Instances such as c5d.4xlarge have locally-attached NVMe SSDs with high IOPS. You can also use EBS volumes with provisioned IOPS (io1). If you are not running performance-critical workloads, you can also choose to use cheaper gp2 EBS volumes. Typically, AWS [gp3](https://aws.amazon.com/about-aws/whats-new/2020/12/introducing-new-amazon-ebs-general-purpose-volumes-gp3/?nc1=h_ls) disks are a good option and have 3000 Baseline IOPS at any disk size.

Recommended disk sizes for Dgraph Zero and Dgraph Alpha:

* Dgraph Zero: 200 GB to 300 GB. Dgraph Zero stores cluster metadata information and maintains a write-ahead log for cluster operations.
* Dgraph Alpha: 250 GB to 750 GB. Dgraph Alpha stores database data, including the schema, indices, and the data values. It maintains a write-ahead log of changes to the database. Your cloud provider may provide better disk performance based on the volume size.
* If you plan to store over 1.1TB per Dgraph Alpha instance, you must increase either the MaxLevels or TableSizeMultiplier. 

Additional recommendations:

* The recommended Linux filesystem is ext4.
* Avoid using shared storage such as NFS, CIFS, and CEPH storage.

### Firewall Rules

Dgraph instances communicate over several ports. Firewall rules should be configured appropriately for the ports documented in [Ports Usage]({{< relref "ports-usage.md" >}}).

Internal ports must be accessible by all Zero and Alpha peers for proper cluster-internal communication. Database clients must be able to connect to Dgraph Alpha external ports either directly or through a load balancer.

Dgraph Zeros can be set up in a private network where communication is only with Dgraph Alphas, database administrators, internal services (such as Prometheus or Jaeger), and possibly developers (see note below). Dgraph Zero's 6080 external port is only necessary for database administrators. For example, it can be used to inspect the cluster metadata (/state), allocate UIDs or set txn timestamps (/assign), move data shards (/moveTablet), or remove cluster nodes (/removeNode). The full docs about Zero's administrative tasks are in [More About Dgraph Zero]({{< relref "deploy/dgraph-zero.md" >}}).

{{% notice "note" %}}
Developers using Dgraph Live Loader or Dgraph Bulk Loader require access to both Dgraph Zero port 5080 and Dgraph Alpha port 9080. When using those tools, consider using them within your environment that has network access to both ports of the cluster.
{{% /notice %}}

### Operating System Tuning

The OS should be configured with the recommended settings to ensure that Dgraph runs properly.

#### File Descriptors Limit

Dgraph can use a large number of open file descriptors. Most operating systems set a default limit that is lower than what is required.

It is recommended to set the file descriptors limit to unlimited. If that is not possible, set it to at least a million (1,048,576) which is recommended to account for cluster growth over time.

### Deployment

A Dgraph instance is run as a single process from a single static binary. It does not require any additional dependencies or separate services in order to run (see the [Supplementary Services]({{< relref "#supplementary-services" >}}) section for third-party services that work alongside Dgraph). A Dgraph cluster is set up by running multiple Dgraph processes networked together.

### Backup Policy

A backup policy is a predefined, set schedule used to schedule backups of information from business applications. A backup policy helps to ensure data recoverability in the event of accidental data deletion, data corruption, or a system outage.

For Dgraph, backups are created using the [backups enterprise feature]({{< relref "/enterprise-features/binary-backups" >}}). You can also create full exports of your data and schema using [data exports]({{< relref "dgraph-administration.md#exporting-database" >}}) available as an open source feature.

We **strongly** recommend that you have a backup policy in place before moving your application to the production phase, and we also suggest that you have a backup policy even for pre-production apps supported by Dgraph database instances running in development, staging, QA or pre-production clusters.

We suggest that your policy include frequent full and incremental backups. Accordingly, we suggest the following backup policy for your production apps:
* [full backup](https://dgraph.io/docs/enterprise-features/binary-backups/#forcing-a-full-backup) every 24hrs
* incremental backup every 2/4hrs

### Supplementary Services

These services are not required for a Dgraph cluster to function but are recommended for better insight when operating a Dgraph cluster.

- [Metrics] and [monitoring][] with Prometheus and Grafana.
- [Distributed tracing][] with Jaeger.

[Metrics]: {{< relref "metrics.md" >}}
[Monitoring]: {{< relref "deploy/monitoring.md" >}}
[Distributed tracing]: {{< relref "tracing.md" >}}
