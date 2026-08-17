---
title: Ports Usage
---

Dgraph cluster nodes use a range of ports to communicate over gRPC and HTTP.
Choose these ports carefully based on your topology and mode of deployment, as
this will impact the access security rules or firewall configurations required
for each port.

## Types of ports

Dgraph Alpha and Dgraph Zero nodes use a variety of gRPC and HTTP ports, as
follows:

- **gRPC-internal-private**: Used between the cluster nodes for internal
 communication and message exchange. Communication using these ports is
 TLS-encrypted.
- **gRPC-external-private**: Used by Dgraph Live Loader and Dgraph Bulk loader
 to access APIs over gRPC.
- **gRPC-external-public**: Used by Dgraph clients to access APIs in a session
 that can persist after a query.
- **HTTP-external-private**: Used for monitoring and administrative tasks.
- **HTTP-external-public:** Used by clients to access APIs over HTTP.

## Default ports used by different nodes

 Dgraph Node Type |  gRPC-internal-private | gRPC-external-private | gRPC-external-public | HTTP-external-private | HTTP-external-public
------------------|------------------------|-----------------------|----------------------|-----------------------|---------------------
       zero       |       5080<sup>1</sup> | 5080<sup>1</sup>      |                      | 6080<sup>2</sup>      |
       alpha      |       7080             |                       |     9080             |                       |    8080
       ratel      |                        |                       |                      |                       |    8000


<sup>1</sup>: Dgraph Zero uses port 5080 for internal communication within the
 cluster, and to support the [data import](../../migration/import-data)
 tools: Dgraph Live Loader and Dgraph Bulk Loader.

<sup>2</sup>: Dgraph Zero uses port 6080 for administrative operations.
Dgraph clients cannot access this port.

Users must modify security rules or open firewall ports depending upon their
underlying network to allow communication between cluster nodes, between the
Dgraph instances, and between Dgraph clients. In general, you should configure
the gRPC and HTTP `external-public` ports for open access by Dgraph clients,
and configure the gRPC-internal ports for open access by the cluster nodes.

**Ratel UI** accesses Dgraph Alpha on the `HTTP-external-public port` (which defaults to localhost:8080) and can be configured to talk to a remote Dgraph cluster. This
way you can run Ratel on your local machine and point to a remote cluster. But,
if you are deploying Ratel along with Dgraph cluster, then you may have to
expose port 8000 to the public.

**Port Offset** To make it easier for users to set up a cluster, Dgraph has
default values for the ports used by Dgraph nodes. To support multiple nodes
running on a single machine or VM, you can set a node to use different ports
using an offset (using the command option `--port_offset`). This command
increments the actual ports used by the node by the offset value provided. You
can also use port offsets when starting multiple Dgraph Zero nodes in a
development environment.

For example, when a user runs Dgraph Alpha with the `--port_offset 2` setting,
then the Alpha node binds to port 7082 (`gRPC-internal-private`), 8082
(`HTTP-external-public`) and 9082 (`gRPC-external-public`), respectively.

**Ratel UI** by default listens on port 8000. You can use the `-port` flag to
configure it to listen on any other port.
