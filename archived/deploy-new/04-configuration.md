+++
title = "Configuration"
weight = 4
type = "docs"
[menu.main]
  identifier = "configuration"
  parent = "deploy"
+++

This guide covers Dgraph configuration options using command-line flags, environment variables, and configuration files.

## Configuration Methods

Dgraph supports three configuration methods (in order of precedence):

1. **Command-line flags** (highest priority)
2. **Environment variables**
3. **Configuration files** (lowest priority)

### Command-Line Flags

```sh
dgraph alpha --my=192.168.1.10:7080 --zero=192.168.1.10:5080 --cache "size-mb=2048"
```

### Environment Variables

Environment variables follow the pattern: `DGRAPH_<COMPONENT>_<FLAG_NAME>`

```sh
export DGRAPH_ALPHA_MY="192.168.1.10:7080"
export DGRAPH_ALPHA_ZERO="192.168.1.10:5080"
export DGRAPH_ALPHA_CACHE="size-mb=2048"
dgraph alpha
```

### Configuration Files

Supported formats: JSON (`.json`), YAML (`.yml`, `.yaml`)

**JSON Example (`config.json`):**
```json
{
  "my": "192.168.1.10:7080",
  "zero": "192.168.1.10:5080",
  "cache": {
    "size-mb": 2048,
    "percentage": "0,65,35"
  },
  "badger": {
    "compression": "zstd:1"
  }
}
```

**YAML Example (`config.yml`):**
```yaml
my: 192.168.1.10:7080
zero: 192.168.1.10:5080
cache:
  size-mb: 2048
  percentage: "0,65,35"
badger:
  compression: "zstd:1"
```

Load with:
```sh
dgraph alpha --config=config.yml
```

---

## Superflags

Superflags are compound configuration options that group related settings. They use semicolon-separated `key=value` pairs.

**Syntax:**
```sh
--superflag "option-a=value; option-b=value; option-c=value"
```

**Example:**
```sh
dgraph alpha --cache "size-mb=2048; percentage=0,65,35"
```

**In config files**, superflags are nested objects:
```yaml
cache:
  size-mb: 2048
  percentage: "0,65,35"
```

---

## Core Configuration Options

### Network Configuration

#### `--my` (Alpha and Zero)

Specifies the address this node advertises to other nodes.

```sh
dgraph alpha --my=192.168.1.10:7080
dgraph zero --my=192.168.1.10:5080
```

**Important:** Use externally-routable IP addresses, not `localhost` in multi-node clusters.

#### `--zero` (Alpha only)

Comma-separated list of Zero addresses for the Alpha to connect to.

```sh
dgraph alpha --zero=zero1:5080,zero2:5080,zero3:5080
```

#### `--port_offset` or `-o`

Increment all port numbers by this offset (useful for running multiple nodes on one host).

```sh
dgraph alpha --my=localhost:7081 -o 1
# Ports become: 7081 (internal), 8081 (HTTP), 9081 (gRPC)
```

### Storage Configuration

#### `--postings` or `-p` (Alpha)

Directory for storing posting lists (main data storage).

```sh
dgraph alpha -p /data/dgraph/p
```

**Default:** `p/` in current working directory

#### `--wal` or `-w` (Alpha and Zero)

Directory for write-ahead logs (WAL).

```sh
dgraph alpha -w /data/dgraph/w
dgraph zero -w /data/dgraph/zw
```

**Default:** `w/` (Alpha), `zw/` (Zero) in current directory

### Badger Storage Engine

The `--badger` superflag configures the underlying Badger storage engine.

**Common Options:**

```sh
dgraph alpha --badger "compression=zstd:3; numgoroutines=16"
```

| Option | Default | Description |
|--------|---------|-------------|
| `compression` | `snappy` | Compression algorithm: `none`, `snappy`, `zstd:level` (1-15) |
| `numgoroutines` | `8` | Concurrent goroutines for Badger operations |

**Compression Recommendations:**
- `snappy` - Fast, moderate compression (default)
- `zstd:1` - Better compression, slightly slower
- `zstd:3` - Best compression, more CPU usage
- `none` - No compression, fastest but uses more disk

### Cache Configuration

The `--cache` superflag controls memory caching.

```sh
dgraph alpha --cache "size-mb=4096; percentage=0,65,35"
```

| Option | Default | Description |
|--------|---------|-------------|
| `size-mb` | `1024` | Total cache size in MB |
| `percentage` | `0,65,35` | Split between PostingList, BlockCache, and IndexCache |

**Percentage Breakdown:**
- First number: Posting list cache (usually 0)
- Second number: Block cache (65% default)
- Third number: Index cache (35% default)

**Guidelines:**
- Allocate 40-50% of total RAM to cache
- Keep percentages summing to 100
- More block cache for read-heavy workloads
- More index cache for filter-heavy queries

### Raft Configuration

The `--raft` superflag configures Raft consensus.

```sh
dgraph alpha --raft "idx=1; snapshot-after-entries=10000"
dgraph zero --raft "idx=1; learner=false"
```

| Option | Default | Description |
|--------|---------|-------------|
| `idx` | auto-assigned | Raft node ID (1-based) |
| `group` | auto-assigned | Raft group ID for Alpha |
| `learner` | `false` | Make this node a read-only learner |
| `snapshot-after-entries` | `10000` | Create Raft snapshot after N entries |
| `snapshot-after-duration` | `30m` | Create Raft snapshot after duration |
| `pending-proposals` | `256` | Max pending mutations (rate limiting) |

### Replication

#### `--replicas` (Zero only)

Number of replicas per shard (must be odd: 1, 3, 5).

```sh
dgraph zero --replicas=3
```

- `--replicas=1`: No replication (not production-safe)
- `--replicas=3`: Standard HA (tolerates 1 failure)
- `--replicas=5`: High HA (tolerates 2 failures)

---

## Performance Tuning

### Query Limits

The `--limit` superflag sets various query and mutation limits.

```sh
dgraph alpha --limit "query-edge=10000000; mutations-nquad=1000000; max-pending-queries=10000"
```

| Option | Default | Description |
|--------|---------|-------------|
| `query-edge` | `1000000` | Max edges returned per query |
| `normalize-node` | `10000` | Max nodes with `@normalize` directive |
| `mutations-nquad` | `1000000` | Max nquads per mutation |
| `query-timeout` | `0ms` | Query timeout (0=infinite) |
| `txn-abort-after` | `5m` | Abort stale transactions after duration |
| `max-pending-queries` | `10000` | Max concurrent queries before 429 errors |

### Memory Management

```sh
# Increase cache for read-heavy workloads
dgraph alpha --cache "size-mb=8192"

# Reduce goroutines if hitting OOM
dgraph alpha --badger "numgoroutines=4"
```

### Disk I/O

```sh
# Use zstd compression for better space efficiency
dgraph alpha --badger "compression=zstd:3"

# Increase Raft snapshot frequency for faster recovery
dgraph alpha --raft "snapshot-after-entries=5000"
```

---

## Security Configuration

### TLS Encryption

The `--tls` superflag enables TLS encryption.

```sh
dgraph alpha --tls "ca-cert=/tls/ca.crt; server-cert=/tls/node.crt; server-key=/tls/node.key; internal-port=true"
```

| Option | Default | Description |
|--------|---------|-------------|
| `ca-cert` | | CA certificate file |
| `server-cert` | | Node certificate file |
| `server-key` | | Node private key file |
| `client-cert` | | Client certificate (for mTLS) |
| `client-key` | | Client private key (for mTLS) |
| `client-auth-type` | `VERIFYIFGIVEN` | Client authentication mode |
| `internal-port` | `false` | Enable TLS on internal ports |
| `use-system-ca` | `true` | Include system CA certificates |

**Client Auth Types:**
- `REQUEST`: Optional client cert, not verified
- `REQUIREANY`: Required, not verified
- `VERIFYIFGIVEN`: Verified if provided (default)
- `REQUIREANDVERIFY`: Required and verified (most secure)

### Access Control

The `--security` superflag controls access restrictions.

```sh
dgraph alpha --security "token=<secret>; whitelist=192.168.1.0/24,10.0.0.0/8"
```

| Option | Default | Description |
|--------|---------|-------------|
| `token` | | Admin auth token for /admin endpoints |
| `whitelist` | `127.0.0.1` | Comma-separated IPs/CIDRs for admin access |

**Whitelist Examples:**
```sh
# Single IP
--security "whitelist=192.168.1.100"

# IP range
--security "whitelist=192.168.1.100:192.168.1.200"

# CIDR blocks
--security "whitelist=10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"

# All IPs (not recommended)
--security "whitelist=0.0.0.0/0"
```

### ACL (Enterprise)

The `--acl` superflag enables access control lists.

```sh
dgraph alpha --acl "secret-file=/secrets/hmac; access-ttl=6h; refresh-ttl=30d"
```

| Option | Default | Description |
|--------|---------|-------------|
| `secret-file` | | HMAC secret file for JWT signing (required) |
| `access-ttl` | `6h` | Access token expiration |
| `refresh-ttl` | `30d` | Refresh token expiration |

---

## Monitoring Configuration

### Metrics and Tracing

The `--trace` superflag configures OpenCensus tracing.

```sh
dgraph alpha --trace "ratio=0.1; jaeger=http://jaeger:14268"
```

| Option | Default | Description |
|--------|---------|-------------|
| `ratio` | `0.01` | Fraction of queries to trace (0.0-1.0) |
| `jaeger` | | Jaeger collector URL |
| `datadog` | | Datadog agent URL |

### Telemetry

The `--telemetry` superflag controls diagnostic reporting.

```sh
dgraph alpha --telemetry "reports=false; sentry=false"
```

| Option | Default | Description |
|--------|---------|-------------|
| `reports` | `true` | Send anonymous usage stats |
| `sentry` | `true` | Send crash reports to Sentry |

---

## Operational Configuration

### Mutation Control

```sh
# Disallow all mutations
dgraph alpha --limit "mutations=disallow"

# Strict mode: only allow mutations on existing predicates
dgraph alpha --limit "mutations=strict"

# Allow all (default)
dgraph alpha --limit "mutations=allow"
```

### GraphQL Configuration

The `--graphql` superflag configures GraphQL behavior.

```sh
dgraph alpha --graphql "introspection=true; debug=false; poll-interval=1s; lambda-url=http://lambda:8686"
```

| Option | Default | Description |
|--------|---------|-------------|
| `introspection` | `true` | Enable schema introspection |
| `debug` | `false` | Return detailed errors to clients |
| `extensions` | `true` | Include extensions in responses |
| `poll-interval` | `1s` | Subscription polling interval |
| `lambda-url` | | URL for @custom resolvers |

---

## Example Configurations

### Development (Single Node)

```yaml
# config-dev.yml
my: localhost:7080
zero: localhost:5080
cache:
  size-mb: 1024
badger:
  compression: snappy
limit:
  mutations: allow
```

### Production (HA, 16GB RAM)

```yaml
# config-prod.yml
my: 192.168.1.10:7080
zero: 192.168.1.10:5080,192.168.1.11:5080,192.168.1.12:5080

cache:
  size-mb: 6144  # ~40% of 16GB RAM
  percentage: "0,65,35"

badger:
  compression: "zstd:1"
  numgoroutines: 16

raft:
  snapshot-after-entries: 10000
  snapshot-after-duration: "30m"

limit:
  query-edge: 10000000
  mutations: strict
  max-pending-queries: 20000

tls:
  ca-cert: /tls/ca.crt
  server-cert: /tls/node.crt
  server-key: /tls/node.key
  internal-port: true

security:
  whitelist: 10.0.0.0/8,192.168.0.0/16

telemetry:
  reports: false
  sentry: false
```

### Enterprise (HA + ACL + Encryption)

```yaml
# config-enterprise.yml
my: 192.168.1.10:7080
zero: 192.168.1.10:5080,192.168.1.11:5080,192.168.1.12:5080

cache:
  size-mb: 12288  # 12GB cache for 32GB RAM

badger:
  compression: "zstd:3"

acl:
  secret-file: /secrets/hmac-secret
  access-ttl: 6h
  refresh-ttl: 30d

encryption:
  key-file: /secrets/enc-key

tls:
  ca-cert: /tls/ca.crt
  server-cert: /tls/node.crt
  server-key: /tls/node.key
  client-cert: /tls/client.crt
  client-key: /tls/client.key
  client-auth-type: REQUIREANDVERIFY
  internal-port: true

security:
  token: ${ADMIN_TOKEN}  # From environment
  whitelist: 10.0.0.0/8

limit:
  mutations: strict
  query-timeout: 30s

trace:
  ratio: 0.05
  jaeger: http://jaeger:14268
```

---

## Configuration Validation

Check your configuration with:

```sh
# Validate config file syntax
dgraph alpha --config=config.yml --help

# Dry-run to see effective configuration
dgraph alpha --config=config.yml 2>&1 | head -n 50
```

---

## Best Practices

1. **Use config files** for complex setups (easier to version control)
2. **Use environment variables** for secrets (never hardcode)
3. **Set resource limits** appropriate to your hardware
4. **Enable TLS** in production (even for internal communication)
5. **Restrict admin access** with IP whitelisting
6. **Monitor configuration changes** (track in git)
7. **Document custom settings** (comment why you deviated from defaults)
8. **Test configuration** in staging before production

---

## Next Steps

- [Security Configuration]({{< relref "security" >}})
- [TLS Setup]({{< relref "security/tls-configuration.md" >}})
- [Monitoring Setup]({{< relref "monitoring.md" >}})
- [CLI Reference]({{< relref "cli-reference.md" >}})
