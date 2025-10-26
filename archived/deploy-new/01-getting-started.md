+++
title = "Getting Started"
weight = 1
type = "docs"
[menu.main]
  identifier = "getting-started"
  parent = "deploy"
+++

This guide helps you get Dgraph up and running quickly.

## Installation Methods

Choose the installation method that best fits your needs:

### Docker (Recommended for Quick Start)

The fastest way to try Dgraph is using the standalone Docker image:

```sh
docker run -d -p "8080:8080" -p "9080:9080" \
  -v ~/dgraph:/dgraph \
  dgraph/standalone:latest
```

This single container runs both Dgraph Zero and Dgraph Alpha for local development.

### Docker Compose (Recommended for Development)

For a more production-like setup on a single machine:

1. Download the docker-compose configuration:
   ```sh
   wget https://github.com/dgraph-io/dgraph/raw/main/contrib/config/docker/docker-compose.yml
   ```

2. Start the cluster:
   ```sh
   docker-compose up -d
   ```

This starts separate Zero, Alpha, and Ratel containers.

### Binary Installation (Linux)

#### Automatic Installation

```sh
curl https://get.dgraph.io -sSf | bash
dgraph version
```

#### Manual Installation

1. Download the latest release from [Dgraph releases](https://github.com/dgraph-io/dgraph/releases)
2. Extract to `/usr/local/bin`:
   ```sh
   sudo tar -C /usr/local/bin -xzf dgraph-linux-amd64-VERSION.tar.gz
   ```
3. Verify installation:
   ```sh
   dgraph version
   ```

### Building from Source

For contributors or custom builds, see [Contributing to Dgraph](https://github.com/dgraph-io/dgraph/blob/master/CONTRIBUTING.md).

## First Steps

After installation:

1. **Access Ratel UI**: Navigate to `http://localhost:8000` in your browser
2. **Connect to Dgraph**: Set server URL to `http://localhost:8080`
3. **Try a query**: Execute your first query in the query tab
4. **Load sample data**: Follow the [Query Language guide](/query-language) to get started

## Next Steps

- [Understand Dgraph Architecture]({{< relref "architecture.md" >}})
- [Choose a Deployment Pattern]({{< relref "deployment-patterns" >}})
- [Configure for Production]({{< relref "production-checklist.md" >}})
