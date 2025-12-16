---
title: Live import
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Live Loader imports data into a running Dgraph cluster using the [dgraph live](/cli/live) command. Unlike [Bulk Loader](bulk-loader), Live Loader can import data into an existing database with prior data and supports upserts for updating existing nodes.

**Use Live Loader when:**
- Importing data into a running cluster
- Updating or adding data to existing nodes
- Loading smaller datasets (for large initial loads, consider [Bulk Loader](bulk-loader))

## Prerequisites

Before importing, ensure you have:
- A running Dgraph cluster
- Data files in RDF (`.rdf`, `.rdf.gz`) or JSON (`.json`, `.json.gz`) format
- A schema file (optional but recommended)

:::note
Live Loader accepts [RDF N-Quad/Triple data](https://www.w3.org/TR/n-quads/) or JSON in plain or gzipped format. See [data migration](import-data) for converting other formats.
:::

## Quick Start

```sh
dgraph live --files ./data.rdf.gz --schema ./schema.txt --alpha localhost:9080
```

## Basic Usage

<Tabs>
<TabItem value="local" label="Local">

```sh
dgraph live \
  --files <path-to-data> \
  --schema <path-to-schema> \
  --alpha localhost:9080
```

</TabItem>
<TabItem value="docker" label="Docker">

```sh
docker run -it --rm -v <local-path-to-data>:/tmp dgraph/dgraph:latest \
  dgraph live \
  --files /tmp/<data-file> \
  --schema /tmp/<schema-file> \
  --alpha <dgraph-alpha-address>:9080
```

</TabItem>
</Tabs>

**Key options:**
- `--alpha` — Dgraph Alpha gRPC endpoint (default: `localhost:9080`). Specify multiple addresses (comma-separated) to distribute load.
- `--files` — Path to data file or directory. When a directory is specified, all `.rdf`, `.rdf.gz`, `.json`, and `.json.gz` files are loaded.
- `--schema` — Path to schema file (use a different extension like `.txt` or `.schema`).

## Upserts: Update Existing Data

Live Loader can update existing nodes using upserts. Use one of these approaches:

### Using `--upsertPredicate`

Specify a predicate that serves as a unique identifier:

```sh
dgraph live \
  --files ./data.rdf.gz \
  --schema ./schema.txt \
  --upsertPredicate xid
```

The upsert predicate must exist in the schema and be indexed.

If you are using `xid` as the upsert predicate name, make sure your schema contains:
```
<xid>: string @index(exact) @upsert .
```

**Example:** If your data contains:
```rdf
<urn:uuid:550e8400-e29b-41d4-a716-446655440000> <http://xmlns.com/foaf/0.1/name> "Alice Smith" .

```

This creates or updates the node where `xid = "urn:uuid:550e8400-e29b-41d4-a716-446655440000>"` and sets its predicate `http://xmlns.com/foaf/0.1/name` to `"Alice Smith"`.


### Using `--xidmap`

Store UID mappings in a local directory for consistent imports:

```sh
dgraph live \
  --files ./data.rdf.gz \
  --schema ./schema.txt \
  --xidmap ./xid-directory
```

Live Loader looks up existing UIDs or stores new mappings in this directory.

## Loading from Cloud Storage

### Amazon S3

Set credentials via environment variables or use [IAM roles](#iam-setup):

| Environment Variable | Description |
|---------------------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key with S3 read permissions |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |

```sh
# Short form (note triple slash)
dgraph live \
  --files s3:///<bucket>/<path> \
  --schema s3:///<bucket>/<path>/schema.txt

# Long form
dgraph live \
  --files s3://s3.<region>.amazonaws.com/<bucket>/<path> \
  --schema s3://s3.<region>.amazonaws.com/<bucket>/<path>/schema.txt
```

#### IAM Setup

Instead of credentials, configure IAM:

1. Create an [IAM Role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create.html) with S3 access
2. Attach it using:
   - [Instance Profile](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html) for EC2
   - [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) for EKS

### MinIO

| Environment Variable | Description |
|---------------------|-------------|
| `MINIO_ACCESS_KEY` | MinIO access key |
| `MINIO_SECRET_KEY` | MinIO secret key |

```sh
dgraph live \
  --files minio://<server>:<port>/<bucket>/<path> \
  --schema minio://<server>:<port>/<bucket>/<path>/schema.txt
```

## Multi-tenancy

When ACL is enabled, provide credentials with `--creds`. By default, data loads into the user's namespace.

```sh
dgraph live \
  --files ./data.rdf.gz \
  --schema ./schema.txt \
  --creds "user=groot;password=password;namespace=0"
```

### Loading into a Specific Namespace

[Guardians of the Galaxy](/admin/admin-tasks/multitenancy#guardians-of-the-galaxy) can load data into any namespace using `--force-namespace`:

```sh
# Load into namespace 123
dgraph live \
  --files ./data.rdf.gz \
  --schema ./schema.txt \
  --creds "user=groot;password=password;namespace=0" \
  --force-namespace 123
```

To preserve namespaces from export files, use `--force-namespace -1`:

```sh
dgraph live \
  --files ./data.rdf.gz \
  --schema ./schema.txt \
  --creds "user=groot;password=password;namespace=0" \
  --force-namespace -1
```

:::note
The target namespace must exist before loading data.
:::

## Encrypted Data

To load encrypted export files, provide the decryption key:

```sh
# Using key file
dgraph live \
  --files ./encrypted-data.rdf.gz \
  --schema ./encrypted-schema.txt \
  --encryption key-file=./encryption.key

# Using HashiCorp Vault
dgraph live \
  --files ./encrypted-data.rdf.gz \
  --schema ./encrypted-schema.txt \
  --vault addr="http://localhost:8200";enc-field="enc_key";enc-format="raw";path="secret/data/dgraph/alpha";role-id-file="./role_id";secret-id-file="./secret_id"
```

:::note
Encrypted exports can be imported into unencrypted Dgraph instances. The `p` directory will only be encrypted if the Alpha has encryption enabled.
:::

## CLI Options Reference

| Flag | Default | Description |
|------|---------|-------------|
| `--files`, `-f` | | Data file or directory path |
| `--schema`, `-s` | | Schema file path |
| `--alpha`, `-a` | `localhost:9080` | Dgraph Alpha gRPC address(es) |
| `--batch`, `-b` | `1000` | N-Quads per mutation batch |
| `--conc`, `-c` | `10` | Concurrent requests to Dgraph |
| `--upsertPredicate`, `-U` | | Predicate for upsert matching |
| `--xidmap`, `-x` | | Directory for UID mappings |
| `--new_uids` | `false` | Assign new UIDs instead of preserving existing |
| `--format` | | Force format (`rdf` or `json`) |
| `--use_compression`, `-C` | `false` | Enable gRPC compression |
| `--creds` | | ACL credentials (`user=;password=;namespace=`) |
| `--force-namespace` | | Load into specific namespace (Guardian only) |
| `--encryption` | | Encryption key file for decryption |
| `--vault` | | Vault configuration for encryption key |

See [dgraph live CLI reference](/cli/live) for the complete list of options.
