+++
date = "2017-03-20T22:25:17+11:00"
title = "Transactions: FAQ"
weight = 1
[menu.main]
    parent = "design-concepts"
+++

Dgraph supports distributed ACID transactions through snapshot isolation and the RAFT consensus protocol. Dgraph is fully transactional, and is tested via Jepsen tests, which is a gold standard to verify transactional consistency.

Dgraph ensure snapshot isolation plus realtime safety: if transaction T1 commits before T2 begins, than the commit timestamp of T1 is strictly less than the start timestamp of T2. This ensures that the sequence of writes on shared data by many processes is reflected in database state.

Snapshot isolation is ensured by maintaining a consistent view of the database at any (relatively recent) point in time. Every read (query) takes place at the point-in-time it was submitted, accesses a consistent snapshot that does not change or include any partial updates due to concurrent writes that are processing or committing.

