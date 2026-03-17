---
title: ACID Transactions
---

ACID is an acronym for
* Atomic
* Consistent
* Isolated
* Durable

If these properties are maintained, there is a guarantee that data updates will not be lost, corrupted or unpredictable. Broadly, an ACID database safely and reliably stores data, but other databases have failure modes where data can be lost or corrupted.

### ACID in Dgraph 
Dgraph supports distributed ACID transactions through snapshot isolation and the RAFT consensus protocol. Dgraph is fully transactional, and is tested via Jepsen tests, which is a gold standard to verify transactional consistency.

Dgraph ensure snapshot isolation plus realtime safety: if transaction T1 commits before T2 begins, than the commit timestamp of T1 is strictly less than the start timestamp of T2. This ensures that the sequence of writes on shared data by many processes is reflected in database state.

Snapshot isolation is ensured by maintaining a consistent view of the database at any (relatively recent) point in time. Every read (query) takes place at the point-in-time it was submitted, accesses a consistent snapshot that does not change or include any partial updates due to concurrent writes that are processing or committing.

