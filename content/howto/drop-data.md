+++
title = "Drop all data"
type = "docs"
[menu.main]
    parent = "howto"
+++


It is possible to drop all data from your Dgraph Cloud backend, and start afresh while retaining the same endpoint.

Be careful, as this operation is not reversible, and all data will be lost. It is highly recommended that you [export]({{< relref "export-data">}}) your data before you drop your data.


## On-Premise
### Drop data and schema

The `/alter` endpoint is used to drop data.

To drop all data and schema:
```sh
$ curl -X POST localhost:8080/alter -d '{"drop_all": true}'
```

To drop all data only (keep schema):
```sh
$ curl -X POST localhost:8080/alter -d '{"drop_op": "DATA"}'
```
The `/alter` endpoint can also be used to drop a specific property or all nodes of a specific type.

To drop property `name`:

```sh
$ curl -X POST localhost:8080/alter -d '{"drop_attr": "name"}'
```

To drop the type `Film`:
```sh
$ curl -X POST localhost:8080/alter -d '{"drop_op": "TYPE", "drop_value": "Film"}'
```
