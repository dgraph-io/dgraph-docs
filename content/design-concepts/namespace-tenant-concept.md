## Namespace or Tenant
A Dgraph `Namespace` (aka Tenant) is a logically separate database within a Dgraph cluster. A Dgraph cluster can host many Namespaces (and this is how the Dgraph "shared" cloud offering works). Each Tenant logs into their own namespace using their own credentials, and sees only their own data. 

There is no mechanism to query in a way that combines data from two namespaces, which simplifies and enforces security in use cases where this is the requirement. An API layer or client would have to pull data from multiple namespaces using different authenticated queries if data needed to be combined.

