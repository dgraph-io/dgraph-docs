+++
date = "2017-03-27:12:00:00Z"
title = "Namespace and Tenant"
type = "docs"
weight = 110
[menu.main]
    parent = "design-concepts"
+++

A Dgraph `Namespace` (aka Tenant) is a logically separate database within a Dgraph cluster. A Dgraph cluster can host many Namespaces (and this is how the Dgraph "shared" cloud offering works). Each user must then into their own namespace using namespace-specific own credentials, and sees only their own data. Note that this usually requires an extra or specific login.

There is no mechanism to query in a way that combines data from two namespaces, which simplifies and enforces security in use cases where this is the requirement. An API layer or client would have to pull data from multiple namespaces using different authenticated queries if data needed to be combined.
