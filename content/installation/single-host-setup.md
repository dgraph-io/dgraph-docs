+++
date = "2017-03-20T22:25:17+11:00"
title = "Basic cluster setup"
weight = 4
type = "docs"
[menu.main]
    parent = "installation"
    identifier = "learning-environment"
+++




The recommended way to get started with Dgraph for local development is by using Docker. There are two main approaches:

## Option 1: Standalone Docker Image (Learning Environment)

The [`dgraph/standalone`](https://hub.docker.com/r/dgraph/standalone) Docker image is the fastest way to get started. This single container runs both Dgraph Zero and Dgraph Alpha, making it ideal for quick testing and development.

Ensure you have [Docker installed](https://www.docker.com/), then run the following command:

```bash
docker run --name dgraph-dev -d -p 8080:8080 -p 9080:9080 \
  -v ~/dgraph:/dgraph \
  dgraph/standalone:latest
```

This command initiates a new Docker container
* `--name dgraph-dev` - creates a persistent container named `dgraph-dev`
* `-d` - runs the container in detached (daemon) mode
* `-p 8080:8080` - maps port 8080 for HTTP connections
* `-p 9080:9080` - maps port 9080 for gRPC connections
* `-v ~/dgraph:/dgraph` - persists data to your local `~/dgraph` directory
* `dgraph/standalone:latest` - uses the official Dgraph standalone image

## Option 2: Docker Compose

For a more production-like setup that separates Zero, Alpha, and Ratel into individual containers, use Docker Compose. This approach gives you better control and is easier to scale.

Create a `docker-compose.yml` file with the following configuration:

```yaml
version: '3.8'
name: dgraph-basic-cluster
services:
  zero:
    image: dgraph/dgraph:latest
    ports:
      - "5080:5080"
      - "6080:6080"
    command: dgraph zero --my=zero:5080
    restart: unless-stopped

  alpha:
    image: dgraph/dgraph:latest
    ports:
      - "8080:8080"
      - "9080:9080"
    command: dgraph alpha --my=alpha:7080 --zero=zero:5080 --security whitelist=0.0.0.0/0
    depends_on:
      - zero
    restart: unless-stopped

  ratel:
    image: dgraph/ratel:latest
    ports:
      - "8000:8000"
    restart: unless-stopped

```

Then start the cluster:

```bash
docker-compose up -d
```

This starts three separate containers:
* **Zero**: Manages cluster membership and assigns UIDs (ports 5080, 6080)
* **Alpha**: Handles queries and mutations (ports 8080, 9080)
* **Ratel**: Web UI for interacting with Dgraph (port 8000)

To stop the cluster:

```bash
docker-compose down
```

To remove all data volumes:

```bash
docker-compose down -v
``` 

### Check your Dgraph cluster health
Verify your Dgraph instance using the `/health` REST endpoint.

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

### Access Ratel UI

Ratel is a web-based UI dashboard for interacting with Dgraph using Dgraph's query language, [DQL]({{<relref "/dgraph-glossary#dql">}}).

**If using Option 1 (Standalone)**: Launch Ratel separately:

```bash
docker run --name ratel -d -p "8000:8000" dgraph/ratel:latest
```

**If using Option 2 (Docker Compose)**: Ratel is already included and will start automatically.

Navigate to Ratel at `http://localhost:8000` and enter `http://localhost:8080` for the "Dgraph Conn String". This will allow Ratel to connect to your local Dgraph instance and execute DQL queries.

![Setting up Ratel](/images/dgraph/quickstart/ratel-docker-connection.png)


