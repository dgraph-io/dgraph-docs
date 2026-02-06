---
title: "GET Request"
description: "Get the structure for GraphQL requests and responses, how to enable compression for them, and configuration options for extensions."

---

<div class="api">

GraphQL request may also be sent using an ``HTTP GET`` operation.

\GET requests must be sent in the following format. The query, variables, and operation are sent as URL-encoded query parameters in the URL.

```
http://localhost:8080/graphql?query={...}&variables={...}&operationName=...
```

- `query` is mandatory
- `variables` is only required if the query contains GraphQL variables.
- `operationName` is only required if there are multiple operations in the query; in which case, operations must also be named.

</div>




