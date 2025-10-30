+++
title = "Advanced Queries with DQL"
weight = 3
[menu.main]
    parent = "cloud"
+++

*You can now [embed DQL queries inside your GraphQL schema](https://dgraph.io/docs/graphql/custom/graphqlpm), which is recommended for most use cases. The rest of this document covers how to connect to your Dgraph Cloud backend with existing Dgraph clients.*

In addition to GraphQL support, Dgraph Cloud also supports running advanced
queries using Dgraph Query Language (DQL) (previously named GraphQL+-).
DQL is based on GraphQL, but adds and removes features to better support graph
database operations. Advanced users can use DQL to send queries and mutations
to Dgraph Cloud's HTTP or gRPC endpoints using the Dgraph client libraries.
To learn more about the Dgraph client libraries, see the 
[client library documentation](https://dgraph.io/docs/clients/). To learn more
about DQL, see [DQL Fundamentals]({{< relref "graphql-fundamentals.md">}})..

If you are getting started with Dgraph Cloud, you should probably start out by
using Dgraph's [GraphQL API]({{< relref "graphql/_index.md">}) instead.
Dgraph's GraphQL API lets you quickly use Dgraph Cloud before moving on to the
advanced features available using DQL.

{{% notice "Note" %}}
Dgraph Cloud's [schema modes](/admin/schema-modes/) let
you configure whether and how schema changes are allowed. To alter your schema 
using the `/alter` HTTP and GRPC endpoints, you'll need to use **Flexible Mode**.
{{% /notice %}}

## Authentication

The APIs documented here all require an API token for access. To learn how to
create an API token, please see [Authentication](/admin/authentication).

### HTTP

You can query your backend with DQL using your cluster's `/query` endpoint. As
an example, if your GraphQL endpoint is `https://frozen-mango.us-west-2.aws.cloud.dgraph.io/graphql`,
then the admin endpoint for the schema is `https://frozen-mango.us-west-2.aws.cloud.dgraph.io/query`.

You can also access the [`/mutate`](https://dgraph.io/docs/mutations/) and
`/commit` endpoints.

For example, let's say you have the following GraphQL schema:
```graphql
type Person {
 name: String! @search(by: [fulltext])
 age: Int
 country: String
}
```

Here is an example of a cURL command with the `/mutate` endpoint:

```
curl -H "Content-Type: application/rdf" -H "x-auth-token: <api-key>" -X POST "<graphql-endpoint>/mutate?commitNow=true" -d $'
{
 set {
    _:x <Person.name> "John" .
    _:x <Person.age> "30" .
    _:x <Person.country> "US" .
 }
}'
```

Here is an example of a cURL command with the `/query` endpoint:

```
curl -H "Content-Type: application/dql" -H "x-auth-token: <api-key>" -XPOST "<graphql-endpoint>/query" -d '{
   queryPerson(func: type(Person))  {
     Person.name
     Person.age
     Person.country
  }
}'
```

### gRPC

Dgraph Cloud is compatible with most existing Dgraph clients. You can use the
helper methods from each library to connect to your backend, passing in a Dgraph
Cloud endpoint and an API token.

Here is an example which uses the [pydgraph client](https://github.com/dgraph-io/pydgraph) to make gRPC requests.

```python
import pydgraph

client_stub = pydgraph.DgraphClientStub.from_slash_endpoint("https://frozen-mango.eu-central-1.aws.cloud.dgraph.io/graphql", "<api-key>")
client = pydgraph.DgraphClient(client_stub)
```

Here is an example of a mutation using the `pydgraph` client:
```python
mut = {
  "Person.name": "John Doe",
  "Person.age": "32",
  "Person.country": "US"
}

txn = client.txn()
try:
  res = txn.mutate(set_obj=mut)
finally:
  txn.discard()
```

Here is an example of a query using the `pydgraph` client:
```python
query = """
{
   queryPerson(func: type(Person))  {
     Person.name
     Person.age
     Person.country
  }
}"""
txn = client.txn()
try:
  res = txn.query(query)
  ppl = json.loads(res.json)
  print(ppl)
finally:
  txn.discard()
```

#### Connecting from Dgraph Clients

Below are snippets to connect to your Dgraph Cloud backend from various Dgraph
clients.

**Python**
```python
import pydgraph

client_stub = pydgraph.DgraphClientStub.from_slash_endpoint("https://frozen-mango.eu-central-1.aws.cloud.dgraph.io/graphql", "<api-key>")
client = pydgraph.DgraphClient(client_stub)
```

**JavaScript**
```javascript
const dgraph = require("dgraph-js");

const clientStub = dgraph.clientStubFromSlashGraphQLEndpoint(
  "https://frozen-mango.eu-central-1.aws.cloud.dgraph.io/graphql",
  "<api-key>"
);
const dgraphClient = new dgraph.DgraphClient(clientStub);
```

**Go**
```golang
// This example uses dgo
conn, err := dgo.DialSlashEndpoint("https://frozen-mango.eu-central-1.aws.cloud.dgraph.io/graphql", "<api-key>")
if err != nil {
  log.Fatal(err)
}
defer conn.Close()
dgraphClient := dgo.NewDgraphClient(api.NewDgraphClient(conn))
```

**Java**
```java
// This example uses dgraph4j
DgraphStub stub = DgraphClient.clientStubFromSlashEndpoint("https://frozen-mango.eu-central-1.aws.cloud.dgraph.io/graphql", "<api-key>");
DgraphClient dgraphClient = new DgraphClient(stub);
```

**C# / .NET**
```c#
var client = new DgraphClient(SlashChannel.Create("frozen-mango.eu-central-1.aws.cloud.dgraph.io:443", "<api-key>"));
```

### Visualizing your Graph with Ratel

You can use Ratel to visualize your Dgraph Cloud backend with DQL. You can host
Ratel yourself, or you can use Ratel online at [Dgraph Play](https://play.dgraph.io/?latest#connection).

To configure Ratel:

1. Click the Dgraph logo in the top left to bring up the connection screen (by default, it has the caption: play.dgraph.io)
2. Enter your backend's host in the Dgraph Server URL field. This is obtained by removing `/graphql` from the end of your `/graphql` endpoint URL. For example, if your `/graphql` endpoint is `https://frozen-mango.us-west-2.aws.cloud.dgraph.io/graphql`, then the host for Ratel is `https://frozen-mango.us-west-2.aws.cloud.dgraph.io`
3. Click the **Connect** button. You should see a green check mark next to the word **Connected**.
4. Click on the **Extra Settings** tab, and then enter your API token into the
 **API Key** field. To create a new API token, see [Authentication](/admin/authentication).
5. Click on the **Continue** button.

You can now run queries and mutations using Ratel, and see visualizations of
your data.

Ratel has certain limitations; it doesn't support backups, modifying ACL or
attempting to remove nodes from the cluster.

### Switching Schema Modes

If you want to use DQL as your primary mode of interaction with the Dgraph Cloud
backend (instead of primarily using the GraphQL API), you can switch your
backend to flexible mode. To learn more, see
[Schema Modes](/admin/schema-modes).
