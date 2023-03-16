## Transactions and Mutations

Borrowing from GraphQL, Dgraph calls writes to the database `Mutations`. As noted elsewhere (MVCC, LSM Trees and Write Ahead Log sections) writes are written persistently to the Write Ahead Log, and ephemerally to a memtable. 

Data is queried from the combination of persistent SST files and ephemeral memtable data structures. The mutations therefore always go into the memtables first (though are also written durably to the WAL). The memtables are the "Level 0" overlay on top of the immutable SST files, to use LSM Tree terminology.

In addition to being written to `Write Ahead Logs`, a mutation also gets stored in memory as an
overlay over immutable `Posting list` in a mutation layer. This mutation layer allows us to iterate
over `Posting`s as though they're sorted, without requiring re-creating the posting list.
