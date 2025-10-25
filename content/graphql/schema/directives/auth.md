+++
title = "@auth"
weight = 1
type = "graphql"
[menu.graphql]
    parent = "directives"
+++

`@auth` allows you to define how to apply authorization rules on the queries/mutation for a type.

Refer to [graphql endpoint security]({{< relref "graphql/security/_index.md">}}), [RBAC rules]({{< relref "RBAC-rules.md">}}) and [Graph traversal rules]({{< relref "graphtraversal-rules.md">}}) for details.


`@auth` directive is not supported on `union` and `@remote` types.

