---
title: Workers
---

### Workers and Worker Pools
Dgraph maintains a fixed set of worker processes (much like threads or goroutines) that retrieve and execute queries in parallel as they are sent over HTTP or gRPC. Dgraph also parallelizes Tasks within a single query execution, to maximize parallelism and more fully utilize system resources. Dgraph is written in the go language, which supports high numbers of parallel goroutines, enabling this approach without creating large numbers of OS threads which would be slower.
