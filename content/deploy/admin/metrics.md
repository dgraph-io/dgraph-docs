+++
date = "2017-03-20T22:25:17+11:00"
title = "Metrics"
description = "Dgraph database helps administrators by providing metrics on Dgraph instance activity, disk activity, server node health, memory, and Raft leadership."
weight = 5
[menu.main]
    parent = "admin"
+++


Dgraph database provides metrics on Dgraph instance activity, disk activity,
server node health, memory, and Raft leadership. It also provides built-in
metrics provided by Go. Dgraph metrics follow the
[metric and label conventions for the Prometheus](https://prometheus.io/docs/practices/naming/)
monitoring and alerting toolkit.

## Activity Metrics

Activity metrics let you track the mutations, queries, and proposals of a Dgraph
instance.

 Metric                                            | Description
 -------                                            | -----------
 `go_goroutines`                                    | Total number of Goroutines currently running in Dgraph.
 `dgraph_active_mutations_total`                    | Total number of mutations currently running.
 `dgraph_pending_proposals_total`                   | Total pending Raft proposals.
 `dgraph_pending_queries_total`                     | Total number of queries in progress.
 `dgraph_num_queries_total{method="Server.Mutate"}` | Total number of mutations run in Dgraph.
 `dgraph_num_queries_total{method="Server.Query"}`  | Total number of queries run in Dgraph.

## Disk metrics

Disk metrics let you track the disk activity of the Dgraph process. Dgraph does
not interact directly with the filesystem. Instead it relies on
[Badger](https://github.com/dgraph-io/badger) to read from and write to disk.

 Metric                          	 | Description
 -------                          	 | -----------
 `badger_disk_reads_total`        | Total count of disk reads in Badger.
 `badger_disk_writes_total`       | Total count of disk writes in Badger.
 `badger_gets_total`              | Total count of calls to Badger's `get`.
 `badger_memtable_gets_total`     | Total count of memtable accesses to Badger's `get`.
 `badger_puts_total`              | Total count of calls to Badger's `put`.
 `badger_read_bytes`              | Total bytes read from Badger.
 `badger_lsm_bloom_hits_total`    | Total number of LSM tree bloom hits.
 `badger_written_bytes`           | Total bytes written to Badger.
 `badger_lsm_size_bytes`          | Total size in bytes of the LSM tree.
 `badger_vlog_size_bytes`         | Total size in bytes of the value log.

## Go Metrics

Go's built-in metrics may also be useful to measure memory usage and garbage
collection time.

Metric                        | Description
-------                        | -----------
`go_memstats_gc_cpu_fraction`  | The fraction of this program's available CPU time used by the GC since the program started.
`go_memstats_heap_idle_bytes`  | Number of heap bytes waiting to be used.
`go_memstats_heap_inuse_bytes` | Number of heap bytes that are in use.

## Health Metrics

Health metrics let you check the health of a server node.

{{% notice "note" %}}
Health metrics are only available for Dgraph Alpha server nodes.
{{% /notice %}}

 Metric                          | Description
 -------                          | -----------
 `dgraph_alpha_health_status`     | Value is 1 when the Alpha node is ready to accept requests; otherwise 0.
 `dgraph_max_assigned_ts`         | This shows the latest max assigned timestamp. All Alpha nodes within the same Alpha group should show the same timestamp if they are in sync.
 `dgraph_txn_aborts_total`        | Shows the total number of server-initiated transaction aborts that have occurred on the Alpha node.
 `dgraph_txn_commits_total`       | Shows the total number of successful commits that have occurred on the Alpha node.
 `dgraph_txn_discards_total`      | Shows the total number of client-initiated transaction discards that have occurred on the Alpha node. This is incremented when the client calls for a transaction discard, such as using the Dgraph Go client's `txn.Discard` function.

## Memory metrics

Memory metrics let you track the memory usage of the Dgraph process. The `idle`
and `inuse` metrics give you a better sense of the active memory usage of the
Dgraph process. The process memory metric shows the memory usage as measured by
the operating system.

By looking at all three metrics you can see how much memory a Dgraph process is
holding from the operating system and how much is actively in use.

 Metric                          | Description
 -------                          | -----------
 `dgraph_memory_idle_bytes`       | Estimated amount of memory that is being held idle that could be reclaimed by the OS.
 `dgraph_memory_inuse_bytes`      | Total memory usage in bytes (sum of heap usage and stack usage).
 `dgraph_memory_proc_bytes`       | Total memory usage in bytes of the Dgraph process. This metric is equivalent to resident set size on Linux.

## Raft leadership metrics

Raft leadership metrics let you track changes in Raft leadership for Dgraph
Alpha and Dgraph Zero nodes in your cluster. These metrics include a group label
along with the node name, so that you can determine which metrics apply to which
Raft groups. 

Metric                             | Description
-------                            | -----------
`dgraph_raft_has_leader`           | Value is 1 when the node has a leader; otherwise 0.
`dgraph_raft_is_leader`            | Value is 1 when the node is the leader of its group; otherwise 0.
`dgraph_raft_leader_changes_total` | The total number of leader changes seen by this node.
