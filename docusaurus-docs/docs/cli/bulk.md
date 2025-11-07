---
title: dgraph bulk
---

The `dgraph bulk` command runs the Dgraph Bulk Loader, which efficiently imports large datasets into Dgraph by bypassing the Alpha server and directly creating posting list files.

## Overview

The Bulk Loader is designed for initial data import of large datasets (millions or billions of triples). It's significantly faster than the Live Loader because it:
- Processes data in parallel using MapReduce-like operations
- Creates posting list files directly without going through a running Alpha
- Shards data across multiple output directories for distributed deployment

:::note
The Bulk Loader should be used for initial import only. For incremental updates on a running cluster, use the [Live Loader](live).
:::

## Usage

```bash
dgraph bulk [flags]
```

## Key Flags

| Flag | Description | Default |
|------|-------------|---------|
| `-f, --files` | Location of *.rdf(.gz) or *.json(.gz) file(s) to load | |
| `-s, --schema` | Location of schema file | |
| `-g, --graphql_schema` | Location of the GraphQL schema file | |
| `--out` | Location to write the final dgraph data directories | `"./out"` |
| `--reduce_shards` | Number of reduce shards (determines number of Alpha nodes) | `1` |
| `--map_shards` | Number of map output shards | `1` |
| `-j, --num_go_routines` | Number of worker threads to use | `1` |
| `--tmp` | Temp directory for on-disk scratch space | `"tmp"` |
| `-z, --zero` | gRPC address for Dgraph Zero | `"localhost:5080"` |
| `--format` | Specify file format (rdf or json) | |
| `--replace_out` | Replace out directory if it exists | `false` |

## Superflags

Bulk uses several [superflags](superflags):

- `--badger` - Badger database options (compression, numgoroutines)
- `--encryption` - Encryption at rest
- `--tls` - TLS configuration
- `--vault` - HashiCorp Vault integration

## Examples

### Basic RDF Import

```bash
dgraph bulk --files data.rdf.gz --schema schema.txt --out ./out
```

### Import Multiple Files

```bash
dgraph bulk --files "data1.rdf.gz,data2.rdf.gz,data3.rdf.gz" \
  --schema schema.txt \
  --out ./out
```

### Import with Multiple Shards

For a 3-node Alpha cluster with replication factor of 3:

```bash
dgraph bulk --files data.rdf.gz \
  --schema schema.txt \
  --reduce_shards 1 \
  --out ./out
```

For a 6-node Alpha cluster (2 groups with 3 replicas each):

```bash
dgraph bulk --files data.rdf.gz \
  --schema schema.txt \
  --reduce_shards 2 \
  --out ./out
```

### Improve Performance

Increase parallelism for faster loading:

```bash
dgraph bulk --files data.rdf.gz \
  --schema schema.txt \
  --num_go_routines 8 \
  --map_shards 4 \
  --reduce_shards 2 \
  --out ./out
```

### JSON Format

```bash
dgraph bulk --files data.json.gz \
  --schema schema.txt \
  --format json \
  --out ./out
```

### With GraphQL Schema

```bash
dgraph bulk --files data.rdf.gz \
  --schema schema.txt \
  --graphql_schema graphql_schema.graphql \
  --out ./out
```

### Encrypted Output

```bash
dgraph bulk --files data.rdf.gz \
  --schema schema.txt \
  --encryption "key-file=./enc-key" \
  --encrypted_out \
  --out ./out
```

## Full Reference

```shell
 Run Dgraph Bulk Loader
Usage:
  dgraph bulk [flags]

Flags:
      --badger string              Badger options (Refer to badger documentation for all possible options)
                                       compression=snappy; Specifies the compression algorithm and compression level (if applicable) for the postings directory. "none" would disable compression, while "zstd:1" would set zstd compression at level 1.
                                       numgoroutines=8; The number of goroutines to use in badger.Stream.
                                    (default "compression=snappy; numgoroutines=8;")
      --cleanup_tmp                Clean up the tmp directory after the loader finishes. Setting this to false allows the bulk loader can be re-run while skipping the map phase. (default true)
      --custom_tokenizers string   Comma separated list of tokenizer plugins
      --encrypted                  Flag to indicate whether schema and data files are encrypted. Must be specified with --encryption or vault option(s).
      --encrypted_out              Flag to indicate whether to encrypt the output. Must be specified with --encryption or vault option(s).
      --encryption string          [Enterprise Feature] Encryption At Rest options
                                       key-file=; The file that stores the symmetric key of length 16, 24, or 32 bytes. The key size determines the chosen AES cipher (AES-128, AES-192, and AES-256 respectively).
                                    (default "key-file=;")
  -f, --files string               Location of *.rdf(.gz) or *.json(.gz) file(s) to load.
      --force-namespace uint       Namespace onto which to load the data. If not set, will preserve the namespace. (default 18446744073709551615)
      --format string              Specify file format (rdf or json) instead of getting it from filename.
  -g, --graphql_schema string      Location of the GraphQL schema file.
  -h, --help                       help for bulk
      --http string                Address to serve http (pprof). (default "localhost:8080")
      --ignore_errors              ignore line parsing errors in rdf files
      --map_shards int             Number of map output shards. Must be greater than or equal to the number of reduce shards. Increasing allows more evenly sized reduce shards, at the expense of increased memory usage. (default 1)
      --mapoutput_mb int           The estimated size of each map file output. Increasing this increases memory usage. (default 2048)
      --new_uids                   Ignore UIDs in load files and assign new ones.
  -j, --num_go_routines int        Number of worker threads to use. MORE THREADS LEAD TO HIGHER RAM USAGE. (default 1)
      --out string                 Location to write the final dgraph data directories. (default "./out")
      --partition_mb int           Pick a partition key every N megabytes of data. (default 4)
      --reduce_shards int          Number of reduce shards. This determines the number of dgraph instances in the final cluster. Increasing this potentially decreases the reduce stage runtime by using more parallelism, but increases memory usage. (default 1)
      --reducers int               Number of reducers to run concurrently. Increasing this can improve performance, and must be less than or equal to the number of reduce shards. (default 1)
      --replace_out                Replace out directory and its contents if it exists.
  -s, --schema string              Location of schema file.
      --skip_map_phase             Skip the map phase (assumes that map output files already exist).
      --store_xids                 Generate an xid edge for each node.
      --tls string                 TLS Client options
                                       ca-cert=; The CA cert file used to verify server certificates. Required for enabling TLS.
                                       client-cert=; (Optional) The Cert file provided by the client to the server.
                                       client-key=; (Optional) The private Key file provided by the clients to the server.
                                       internal-port=false; (Optional) Enable inter-node TLS encryption between cluster nodes.
                                       server-name=; Used to verify the server hostname.
                                       use-system-ca=true; Includes System CA into CA Certs.
                                    (default "use-system-ca=true; internal-port=false;")
      --tmp string                 Temp directory used to use for on-disk scratch space. Requires free space proportional to the size of the RDF file and the amount of indexing used. (default "tmp")
      --vault string               Vault options
                                       acl-field=; Vault field containing ACL key.
                                       acl-format=base64; ACL key format, can be 'raw' or 'base64'.
                                       addr=http://localhost:8200; Vault server address (format: http://ip:port).
                                       enc-field=; Vault field containing encryption key.
                                       enc-format=base64; Encryption key format, can be 'raw' or 'base64'.
                                       path=secret/data/dgraph; Vault KV store path (e.g. 'secret/data/dgraph' for KV V2, 'kv/dgraph' for KV V1).
                                       role-id-file=; Vault RoleID file, used for AppRole authentication.
                                       secret-id-file=; Vault SecretID file, used for AppRole authentication.
                                    (default "addr=http://localhost:8200; role-id-file=; secret-id-file=; path=secret/data/dgraph; acl-field=; acl-format=base64; enc-field=; enc-format=base64")
      --version                    Prints the version of Dgraph Bulk Loader.
      --xidmap string              Directory to store xid to uid mapping
  -z, --zero string                gRPC address for Dgraph zero (default "localhost:5080")

Use "dgraph bulk [command] --help" for more information about a command.
```

## Output Structure

After bulk loading, the `--out` directory will contain subdirectories for each group:

```
out/
├── 0/
│   └── p/            # Posting lists for group 1
│       ├── 000000.sst
│       ├── 000001.sst
│       └── MANIFEST
└── 1/
    └── p/            # Posting lists for group 2 (if reduce_shards > 1)
        ├── 000000.sst
        ├── 000001.sst
        └── MANIFEST
```

Each subdirectory corresponds to an Alpha group and should be copied to the appropriate Alpha node's `-p` directory.

## Performance Tuning

### Memory Considerations

The Bulk Loader is memory-intensive. Key parameters affecting memory:

- `--num_go_routines`: More threads = faster but more RAM
- `--map_shards`: More shards = better distribution but more RAM
- `--mapoutput_mb`: Larger values = more RAM per map task

**Rule of thumb**: For N GB of input data, allocate at least N GB of RAM.

### Optimizing for Large Datasets

For datasets > 100 million triples:

```bash
dgraph bulk --files data.rdf.gz \
  --schema schema.txt \
  --num_go_routines 16 \
  --map_shards 8 \
  --reduce_shards 3 \
  --mapoutput_mb 4096 \
  --out ./out
```

### Disk Space Requirements

Ensure adequate disk space:
- Input data size
- 2-3x input size for temporary files (can be controlled with `--tmp`)
- Output size (varies based on indexing, typically 1-2x input size)

## Workflow

1. **Prepare Data**: RDF or JSON format, optionally compressed (.gz)
2. **Prepare Schema**: Define types, indexes, and constraints
3. **Run Bulk Loader**: Process and shard data
4. **Deploy Output**: Copy each group's directory to corresponding Alpha nodes
5. **Start Cluster**: Launch Zero and Alpha nodes

## Common Issues

### Out of Memory

- Reduce `--num_go_routines`
- Reduce `--map_shards`
- Reduce `--mapoutput_mb`
- Add more RAM to the system

### Slow Performance

- Increase `--num_go_routines` (if RAM allows)
- Increase `--map_shards` for better parallelism
- Use faster storage for `--tmp` directory

### Invalid Data

- Use `--ignore_errors` to skip malformed lines
- Validate RDF/JSON format before bulk loading

## See Also

- [Live Loader](live) - For incremental updates
- [Data Migration](../migration/import-data) - Migration strategies
- [Schema](../dql/dql-schema) - Schema definition
- [Bulk Loader Guide](../migration/bulk-loader) - Detailed bulk loading guide

