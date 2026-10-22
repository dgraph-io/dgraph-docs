---
title: View Cluster State
---

The cluster state provides detailed information about your cluster's current state, including group membership, predicate distribution (sharding), and cluster metadata. You can query cluster state using either the HTTP endpoint or the GraphQL Admin API on Alpha.

## Query Cluster State

### Using HTTP Endpoint

Query the `/state` endpoint:

```sh
curl http://localhost:8080/state | jq
```

### Using GraphQL Admin API

You can also query cluster state using the GraphQL `state` query on the `/admin` endpoint (port 8080):

```graphql
query {
  state {
    groups {
      id
      members {
        id
        groupId
        addr
        leader
        amDead
      }
      tablets {
        predicate
        groupId
        space
        readOnly
      }
    }
    zeros {
      id
      groupId
      addr
      leader
    }
    maxUID
    maxTxnTs
    maxRaftId
    cid
    license {
      enabled
      maxNodes
      expiryTs
    }
  }
}
```

## Response Information

The `/state` endpoint returns a JSON document containing:

- **Cluster membership**: Instances that are part of the cluster
- **Group information**: Number of instances in Zero group and each Alpha group
- **Leadership**: Current leader of each group
- **Predicate distribution**: Which predicates (tablets) belong to which groups
- **Predicate sizes**: Estimated size in bytes of each predicate
- **Enterprise license**: License information and status
- **Transaction metadata**: Max leased transaction ID
- **UID metadata**: Max leased UID
- **Cluster ID**: Unique cluster identifier (CID)

## Example Response

Here's an example JSON response for a cluster with three Alpha nodes and three Zero nodes:

```json
{
  "counter": "22",
  "groups": {
    "1": {
      "members": {
        "1": {
          "id": "1",
          "groupId": 1,
          "addr": "alpha2:7082",
          "leader": true,
          "amDead": false,
          "lastUpdate": "1603350485",
          "clusterInfoOnly": false,
          "forceGroupId": false
        },
        "2": {
          "id": "2",
          "groupId": 1,
          "addr": "alpha1:7080",
          "leader": false,
          "amDead": false,
          "lastUpdate": "0",
          "clusterInfoOnly": false,
          "forceGroupId": false
        },
        "3": {
          "id": "3",
          "groupId": 1,
          "addr": "alpha3:7083",
          "leader": false,
          "amDead": false,
          "lastUpdate": "0",
          "clusterInfoOnly": false,
          "forceGroupId": false
        }
      },
      "tablets": {
        "dgraph.cors": {
          "groupId": 1,
          "predicate": "dgraph.cors",
          "force": false,
          "space": "0",
          "remove": false,
          "readOnly": false,
          "moveTs": "0"
        },
        "dgraph.graphql.schema": {
          "groupId": 1,
          "predicate": "dgraph.graphql.schema",
          "force": false,
          "space": "0",
          "remove": false,
          "readOnly": false,
          "moveTs": "0"
        },
        "dgraph.type": {
          "groupId": 1,
          "predicate": "dgraph.type",
          "force": false,
          "space": "0",
          "remove": false,
          "readOnly": false,
          "moveTs": "0"
        }
      },
      "snapshotTs": "22",
      "checksum": "18099480229465877561"
    }
  },
  "zeros": {
    "1": {
      "id": "1",
      "groupId": 0,
      "addr": "zero1:5080",
      "leader": true,
      "amDead": false,
      "lastUpdate": "0",
      "clusterInfoOnly": false,
      "forceGroupId": false
    },
    "2": {
      "id": "2",
      "groupId": 0,
      "addr": "zero2:5082",
      "leader": false,
      "amDead": false,
      "lastUpdate": "0",
      "clusterInfoOnly": false,
      "forceGroupId": false
    },
    "3": {
      "id": "3",
      "groupId": 0,
      "addr": "zero3:5083",
      "leader": false,
      "amDead": false,
      "lastUpdate": "0",
      "clusterInfoOnly": false,
      "forceGroupId": false
    }
  },
  "maxUID": "10000",
  "maxTxnTs": "10000",
  "maxRaftId": "3",
  "removed": [],
  "cid": "2571d268-b574-41fa-ae5e-a6f8da175d6d",
  "license": {
    "user": "",
    "maxNodes": "18446744073709551615",
    "expiryTs": "1605942487",
    "enabled": true
  }
}
```

## Understanding the Response

### Group Members

The response shows node members with their addresses and HTTP port numbers:

- **Group 1 members** (Alpha nodes):
  - alpha2:7082, id: 1, leader
  - alpha1:7080, id: 2
  - alpha3:7083, id: 3
- **Group 0 members** (Dgraph Zero nodes):
  - zero1:5080, id: 1, leader
  - zero2:5082, id: 2
  - zero3:5083, id: 3

### maxUID

The current maximum lease of UIDs used for blank node UID assignment. This increments in batches of 10,000 IDs. Once the maximum lease is reached, another 10,000 IDs are leased. In the event that the Zero leader is lost, the new leader starts a new lease from `maxUID`+1. Any UIDs lost between these leases will never be used for blank-node UID assignment.

An admin can use the Zero endpoint HTTP GET `/assign?what=uids&num=1000` to reserve a range of UIDs (in this case, 1000) to use externally. Zero will **never** use these UIDs for blank node UID assignment, so the user can use the range to assign UIDs manually to their own data sets.

### maxTxnTs

The current maximum lease of transaction timestamps used to hand out start timestamps and commit timestamps. This increments in batches of 10,000 IDs. After the max lease is reached, another 10,000 IDs are leased. If the Zero leader is lost, then the new leader starts a new lease from `maxTxnTs`+1. Any lost transaction IDs between these leases will never be used.

An admin can use the Zero endpoint HTTP GET `/assign?what=timestamps&num=1000` to increase the current transaction timestamp (in this case, by 1000). This is mainly useful in special-case scenarios; for example, using an existing `-p directory` to create a fresh cluster to be able to query the latest data in the DB.

### maxRaftId

The number of Zeros available to serve as a leader node. Used by the [RAFT](../../design-concepts/raft) consensus algorithm.

### CID

This is a unique UUID representing the *cluster-ID* for this cluster. It is generated during the initial DB startup and is retained across restarts.

### Enterprise License

License information including:
- Enabled status
- `maxNodes`: Maximum number of nodes allowed (unlimited if not restricted)
- License expiration, shown in seconds since the Unix epoch

### Tablets (Predicates)

The `tablets` section shows which predicates are assigned to which groups. Each tablet entry includes:
- `groupId`: The group that owns this predicate
- `predicate`: The predicate name
- `space`: Estimated size
- `readOnly`: Whether the predicate is read-only
- `moveTs`: Timestamp of last move operation

:::note
The terms "tablet", "predicate", and "edge" are currently synonymous. In future, Dgraph might improve data scalability to shard a predicate into separate tablets that can be assigned to different groups.
:::

