+++
date = "2017-03-20T22:25:17+11:00"
title = "Consistency Model"
weight = 25
[menu.main]
    parent = "design-concepts"
+++

## Dgraph supports MVCC, Read Snapshots and Distributed ACID transactions
Multi-version concurrency control (MVCC) is a technique where many versions of data are written (but never modified) on disk, so many versions exist. This helps control concurrency because the database is queried at a particular "timestamp" for the duration of one query to provide snapshot isolation and ensure data is consistent for that transaction. (Note that MVCC is losely related to LSM trees - in LSM parlance, data is "logged" to write-only files, which are later merged via Log Compaction.) 

Writes are faster with MVCC because data is always written by flushing a larger in-memory buffer (a memtable) to new, contiguous files (SST files), and newer data obscures or replaces older data. Consistent updates from each transaction share a logical commit timestamp (a 64 bit, increasing number loosely correlated to wall clock time), and all reads occur "at a point in time" meaning any read accesses a known, stable set of committed data using these same commit timestamps. New or in-process commits are associated with a later timestamp so they do not affect running queries at earlier timestamps. This allows pure queries (reads) to execute without any locks.

One special set of structures are "memtables" which are also referred to as being Level 0 of the LSM tree. These are buffers for fast writes, which later are flushed to on-disk files called SSTs.

## Dgraph transactions are cluster-wide (not key-only, or any other non-ACID version of transactions)
Dgraph uses the RAFT protocol to synchronize updates and ensure updates are durably written to a majority of alpha nodes in a cluster before the transaction is considered successful. RAFT ensures true, distributed, cluster wide transactions across multiple nodes, keys, edges, indexes and facets. Dgraph provides true ACID transactions, and does not impose limitations on what can be in a transaction: a transaction can involve multiple predicates, multiple nodes, multiple keys and even multiple shards. 

## Transactions are lockless
Dgraph transactoins do not use locks, allowing fast, distributed transactions.

For reads, queries execute at a particular timestamp based on snapshot isolation, which isolates reads from any concurrent write activity. All reads access snapshots across the entire cluster, seeing all previously committed transactions in full, regardless of which alpha node received earlier queries.

Writes use optimistic lock semantics, where a transaction will be aborted if another (concurrent) transaction updates exactly the same data (same edge on the same node) first. This will be reported as an "aborted" transaction to the caller.

Dgraph ensures monotonically increasing transaction timestamps to sequence all updates in the database. This provides serializability: if any transaction Tx1 commits before Tx2 starts, then Ts_commit(Tx1) < Ts_start(Tx2), and in turn a read at any point in time can never see Tx1 changes but not Tx2 changes.

Dgraph also ensures proper read-after-write semantics. Any commit at timestamp Tc is guaranteed to be seen by a read at timestamp Tr by any client, if Tr >= Tc.

### Terminology

- **Snapshot isolation:** all reads see a consistent view of the database at the point in time when the read was submitted
- **Oracle:** a logical process that tracks timestamps and which data (keys, predicates, etc.) has been committed or is being modified. The oracle hands out timestamps and aborts transactions if another transaction has modified its data.
- **RAFT:** a well-known consistency algorithm to ensure distributed processes durably store data
- **Write-Ahead Log:** Also WAL. A fast log of updates on each alpha that ensures buffered in-memory structures are persisted.
- **Proposal:** A process within the RAFT algorithm to track possible updates during the consensus process.
- **SST:** Persistent files comprising the LSM tree, together with memtables.
- **Memtable:** An in-memory version of an SST, supporting fast updates. Memtables are mutable, and SSTs are immutable.
- **Log Compaction:** The process of combining SSTs into newer SSTs while eliminating obsolte data and reclaiming disk space.
- **Timestamp:** Or point in time. A numeric counter representing the sequential order of all transactions, and indicating when a transaction became valid and query-able.
- **Optimistic Lock:** a logical process whereby all transactions execute without blocking on other transactions, and are aborted if there is a conflict. Aborted transactions should typically be retried if they occur.
- **Pessimistic Lock:** a process, not used in Dgraph, where all concurrent transactions mutating the same data except one block and wait for each other to complete. 
- **ACID** An acronym representing attributes of true transactions: Atomic, Consistent, Isolated, and Durable