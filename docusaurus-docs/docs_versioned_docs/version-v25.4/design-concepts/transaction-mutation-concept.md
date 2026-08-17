---
title: Transaction and Mutation
---


Borrowing from GraphQL, Dgraph calls writes to the database `Mutations`. As noted elsewhere (MVCC, LSM Trees and Write Ahead Log sections) writes are written persistently to the Write Ahead Log, and ephemerally to a memtable.

Data is queried from the combination of persistent SST files and ephemeral memtable data structures. The mutations therefore always go into the memtables first (though are also written durably to the WAL). The memtables are the "Level 0" in the LSM Tree, and conceptually sit on top of the immutable SST files.
