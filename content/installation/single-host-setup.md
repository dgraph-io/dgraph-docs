+++
date = "2017-03-20T22:25:17+11:00"
title = "Learning Environment"
weight = 2
type = "docs"
[menu.main]
    parent = "installation"
    identifier = "learning-environment"
+++




The recommended way to get started with Dgraph for local development is by using
the official Dgraph Docker image.

### Start a standalone Dgraph cluster

The [`dgraph/standalone`](https://hub.docker.com/r/dgraph/standalone) Docker image has everything needed to run Dgraph locally.

Ensure you have [Docker installed](https://www.docker.com/), then run the following command to start a local Dgraph instance:

```bash
docker run --name dgraph-dev -d  -p 8080:8080 -p 9080:9080 dgraph/standalone:latest
```

This will create a local Dgraph instance and expose the ports necessary to connect to Dgraph via HTTP and gRPC. Specifically:

* `docker run` - initiates a new Docker container
* `--name dgraph-dev` - create a persistent docker imane named `dgraph-dev`
* `-d` - uses daemon mode
* `-p 8080:8080` - maps port 8080 from the host machine to port 8080 in the Docker container to allow Dgraph HTTP connections
* `-p 9080:9080` - maps port 9080 from the host machine to port 9080 in the Docker container to allow Dgraph gRPC connections
* `dgraph/standalone:latest` - specifies the Docker image to use, this is the official Dgraph image 

### Check your Dgraph cluster health
Verify your Dgraph instance using the `/heatlh` REST endpoint.

```shell
curl http://localhost:8080/health | jq
```
The command should return basic cluster information:
```json
[
  {
    "instance": "alpha",
    "address": "localhost:7080",
    "status": "healthy",
    "group": "1",
    "version": "v24.1.5",
    "uptime": 11,
    "lastEcho": 1761430795,
    "ongoing": [
      "opRollup"
    ],
    "ee_features": [
      "backup_restore",
      "cdc"
    ],
    "max_assigned": 30002
  }
]
```

### Connect Ratel
Ratel is a web-based UI dashboard for interacting with Dgraph using Dgraph's query language, [DQL]({{<relref "/dgraph-glossary#dql">}}).

Optionnaly, launch Ratel using the dgraph/ratel docker image :

``` sh
    docker run --name ratel  -d -p "8000:8000"  dgraph/ratel:latest
```

Navigate to Ratel at `http://localhosr:8000` and enter `http://localhost:8080` for the "Dgraph Conn String".
This will allow Ratel to connect to our local Dgraph instance and execute DQL queries.

   ![Setting up Ratel](/images/dgraph/quickstart/ratel-docker-connection.png)


