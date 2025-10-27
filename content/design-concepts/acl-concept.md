+++
date = "2017-03-27T12:00:00Z"
title = "ACLs"
type = "docs"
weight = 10
[menu.main]
    parent = "design-concepts"
+++

ACLs are a typical mechanism to list who can access what, specifying either users or roles and what they can access. ACLs help determine who is "authorized" to access what.

Dgraph Access Control Lists (ACLs) are sets of permissions for which `Relationships` a user may access. Recall that Dgraph is "predicate based" so all data is stored in and is implicit in relationships. This allows relationship-based controls to be very powerful in restricting a graph based on roles (RBAC).

Note that the Dgraph multi-tenancy feature relies on ACLs to ensure each tenant can only see their own data in one server.

Using ACLs requires a client to authenticate (log in) differently and specify credentials that will drive which relationships are visible in their view of the graph database.
