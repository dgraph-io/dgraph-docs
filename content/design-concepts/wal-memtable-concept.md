## Write Ahead Logs (WAL) and Memtables
Per the RAFT (and MVCC) approach, transactions write data to a `Write-Ahead Log` to ensure it is durably stored. Soon after commit, data is also updated in the `memtables` which are buffers holding all new data. The `memtables` are mutable, unlike the SST files written to disk which hold most data. Once full, memtables are flushed to disk and become SST files. See Log Compaction for more details on this process.

In the event of a system crash, the persistent data in the Write Ahead Logs is replayed to rebiuld the memtables and restore the full state from before the crash.
