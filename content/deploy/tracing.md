+++
date = "2017-03-20T22:25:17+11:00"
title = "Tracing"
weight = 6
[menu.main]
    parent = "admin"
+++

Dgraph is integrated with [OpenCensus](https://opencensus.io/zpages/) to collect distributed traces from the Dgraph cluster.

Trace data is always collected within Dgraph. You can adjust the trace sampling rate for Dgraph queries using the `--trace` [superflag's]({{< relref "deploy/cli-command-reference.md" >}}) `ratio` option when running Dgraph Alpha nodes. By default, `--trace ratio`  is set to 0.01 to trace 1% of queries.

## Examining Traces with zPages

The most basic way to view traces is with the integrated trace pages.

OpenCensus's [zPages](https://opencensus.io/zpages/) are accessible via the Zero or Alpha HTTP port at `/z/tracez`.

## Examining Traces with Jaeger

Jaeger collects distributed traces and provides a UI to view and query traces across different services. This provides the necessary observability to figure out what is happening in the system.

Dgraph can be configured to send traces directly to a Jaeger collector with the `trace` superflag's `jaeger` option. For example, if the Jaeger collector is running on `http://localhost:14268`, then pass this option to the Dgraph Zero and Dgraph Alpha instances as `--trace jaeger=http://localhost:14268`.

See [Jaeger's Getting Started docs](https://www.jaegertracing.io/docs/getting-started/) to get up and running with Jaeger.

### Setting up multiple Dgraph clusters with Jaeger

Jaeger allows you to examine traces from multiple Dgraph clusters. To do this, use the `--collector.tags` on a Jaeger collector to set custom trace tags. For example, run one collector with `--collector.tags env=qa` and then another collector with `--collector.tags env=dev`. In Dgraph, set the `--trace jaeger` option in the Dgraph QA cluster to the first collector and set this option in the Dgraph Dev cluster to the second collector.
You can run multiple Jaeger collector components for the same single Jaeger backend (e.g., many Jaeger collectors to a single Cassandra backend). This is still a single Jaeger installation but with different collectors customizing the tags per environment.

Once you have this configured, you can filter by tags in the Jaeger UI. Filter traces by tags matching `env=dev`:

{{% load-img "/images/jaeger-ui.png" "Jaeger UI" %}}

Every trace has your custom tags set under the “Process” section of each span:

{{% load-img "/images/jaeger-server-query.png" "Jaeger Query" %}}

Filter traces by tags matching `env=qa`:

{{% load-img "/images/jaeger-json.png" "Jaeger JSON" %}}

{{% load-img "/images/jaeger-server-query-2.png" "Jaeger Query Result" %}}

### Other tags available

The OpenTrace information collected by Dgraph and displayed in Jaeger contains various messages and metadata that can also be filtered by tag. Below is a list of information that is in Jaeger as a tag.

#### Tag message and status.message

This tag you will filter out based on the message.
e.g:

```php
message="Found Raft entries: 1"
message="Found a conflict. Aborting."
message="Aborting txn due to context timing out."
message="Snapshot proposed: Done"
message="Saved to storage"
message="Applying schema and types"
message="Found pending transactions. Retry later."
message="Starting stream list orchestrate"
message="Waiting for checksum match"
message="Done waiting for checksum match"
message="Query parsed"
message="Start".

status.message="grpc: the client connection is closing"
status.message="Cannot get linearized read (time expired or no configured leader)"
status.message="No node has been set up yet"
status.message="Raft group mismatch"
status.message="Response not compressed"
status.message="transaction could not be aborted"
status.message="Failed to read key block"
status.message="Failed to read cert block"
status.message="Assigning IDs is only allowed on leader."
status.message="Nothing to be leased"
status.message="No healthy connection found to Leader of group zero"
status.message="Only leader can decide to commit or abort"
status.message="Raft isn't initialized yet."
status.message="Unable to find group"
```

#### Tag error

This tag you will filter out based on error status.

e.g: `error=true`

#### Tag status.code

This tag you will filter out based on status code 0, 1 or 2.

e.g: `status.code=1`

#### Tag ns(namespace)

This tag you will filter out only the given namespace.

e.g: `ns=7`

#### Tag committed

e.g: `committed=true`

#### Tag funcName

available attributes

```php
handleHasFunction, n.proposeAndWait, dgraph.Execute, resolveMutation,
resolveQuery,resolveCustomDQLQuery, RequestResolver.Resolve, resolveHTTP,
query.ProcessQuery, n.proposeAndWait, processSort, handleValuePostings,
handleUidPostings, handleRegexFunction, handleCompareFunction, handleMatchFunction
filterGeoFunction, handleHasFunction

"expandSubgraph: " + Predicate
e.g: funcName=expandSubgraph: dgraph.type

"query.ProcessGraph" + suffix
"processTask" + q.Attr
```

For you to be able to see something you must execute a query corresponding to the function.
For example, fun a has() function in a query and use the tag bellow.

e.g: `funcName=handleHasFunction`

To learn more about Jaeger, see [Jaeger's Deployment Guide](https://www.jaegertracing.io/docs/deployment/).
