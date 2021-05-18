+++
date = "2017-03-20T22:25:17+11:00"
title = "Bulk Loader"
weight = 12
[menu.main]
    parent = "fast-data-loading"
+++

Dgraph Bulk Loader serves a similar purpose to the Dgraph Live Loader, but can
only be used to load data into a new cluster. It cannot be run on an existing
Dgraph cluster. Dgraph Bulk Loader is **considerably faster** than the Dgraph
Live Loader and is the recommended way to perform the initial import of large
datasets into Dgraph.

Only one or more Dgraph Zeros should be running for bulk loading. Dgraph Alphas
will be started later.

You can [read some technical details](https://blog.dgraph.io/post/bulkloader/)
about the bulk loader on the blog.

{{% notice "warning" %}}
Don't use the Bulk loader once the Dgraph cluster is up and running. Use it to import
your existing data to a new cluster.
{{% /notice %}}

{{% notice "tip" %}}
It's crucial to tune the bulk loader's flags to get good performance. See the
next section for details.
{{% /notice %}}

## Settings

{{% notice "note" %}} Bulk Loader only accept [RDF N-Quad/Triple
data](https://www.w3.org/TR/n-quads/) or JSON in plain or gzipped format. Data
in other formats must be converted.{{% /notice %}}

```sh
$ dgraph bulk --help # To see the available flags.

# Read RDFs or JSON from the passed file.
$ dgraph bulk -f <path-to-gzipped-RDF-or-JSON-file> ...

# Read multiple RDFs or JSON from the passed path.
$ dgraph bulk -f <./path-to-gzipped-RDF-or-JSON-files> ...

# Read multiple files strictly by name.
$ dgraph bulk -f <file1.rdf, file2.rdf> ...

```

- **Reduce shards**: Before running the bulk load, you need to decide how many
Alpha groups will be running when the cluster starts. The number of Alpha groups
will be the same number of reduce shards you set with the `--reduce_shards`
flag. For example, if your cluster will run 3 Alpha with 3 replicas per group,
then there is 1 group and `--reduce_shards` should be set to 1. If your cluster
will run 6 Alphas with 3 replicas per group, then there are 2 groups and
`--reduce_shards` should be set to 2.

- **Map shards**: The `--map_shards` option must be set to at least what's set for
`--reduce_shards`. A higher number helps the bulk loader evenly distribute
predicates between the reduce shards.

For example:

```sh
$ dgraph bulk -f goldendata.rdf.gz -s goldendata.schema --map_shards=4 --reduce_shards=2 --http localhost:8000 --zero=localhost:5080
```

```
{
	"DataFiles": "goldendata.rdf.gz",
	"DataFormat": "",
	"SchemaFile": "goldendata.schema",
	"DgraphsDir": "out",
	"TmpDir": "tmp",
	"NumGoroutines": 4,
	"MapBufSize": 67108864,
	"ExpandEdges": true,
	"SkipMapPhase": false,
	"CleanupTmp": true,
	"NumShufflers": 1,
	"Version": false,
	"StoreXids": false,
	"ZeroAddr": "localhost:5080",
	"HttpAddr": "localhost:8000",
	"IgnoreErrors": false,
	"MapShards": 4,
	"ReduceShards": 2
}
The bulk loader needs to open many files at once. This number depends on the size of the data set loaded, the map file output size, and the level of indexing. 100,000 is adequate for most data set sizes. See `man ulimit` for details of how to change the limit.
Current max open files limit: 1024
MAP 01s rdf_count:176.0 rdf_speed:174.4/sec edge_count:564.0 edge_speed:558.8/sec
MAP 02s rdf_count:399.0 rdf_speed:198.5/sec edge_count:1.291k edge_speed:642.4/sec
MAP 03s rdf_count:666.0 rdf_speed:221.3/sec edge_count:2.164k edge_speed:718.9/sec
MAP 04s rdf_count:952.0 rdf_speed:237.4/sec edge_count:3.014k edge_speed:751.5/sec
MAP 05s rdf_count:1.327k rdf_speed:264.8/sec edge_count:4.243k edge_speed:846.7/sec
MAP 06s rdf_count:1.774k rdf_speed:295.1/sec edge_count:5.720k edge_speed:951.5/sec
MAP 07s rdf_count:2.375k rdf_speed:338.7/sec edge_count:7.607k edge_speed:1.085k/sec
MAP 08s rdf_count:3.697k rdf_speed:461.4/sec edge_count:11.89k edge_speed:1.484k/sec
MAP 09s rdf_count:71.98k rdf_speed:7.987k/sec edge_count:225.4k edge_speed:25.01k/sec
MAP 10s rdf_count:354.8k rdf_speed:35.44k/sec edge_count:1.132M edge_speed:113.1k/sec
MAP 11s rdf_count:610.5k rdf_speed:55.39k/sec edge_count:1.985M edge_speed:180.1k/sec
MAP 12s rdf_count:883.9k rdf_speed:73.52k/sec edge_count:2.907M edge_speed:241.8k/sec
MAP 13s rdf_count:1.108M rdf_speed:85.10k/sec edge_count:3.653M edge_speed:280.5k/sec
MAP 14s rdf_count:1.121M rdf_speed:79.93k/sec edge_count:3.695M edge_speed:263.5k/sec
MAP 15s rdf_count:1.121M rdf_speed:74.61k/sec edge_count:3.695M edge_speed:246.0k/sec
REDUCE 16s [1.69%] edge_count:62.61k edge_speed:62.61k/sec plist_count:29.98k plist_speed:29.98k/sec
REDUCE 17s [18.43%] edge_count:681.2k edge_speed:651.7k/sec plist_count:328.1k plist_speed:313.9k/sec
REDUCE 18s [33.28%] edge_count:1.230M edge_speed:601.1k/sec plist_count:678.9k plist_speed:331.8k/sec
REDUCE 19s [45.70%] edge_count:1.689M edge_speed:554.4k/sec plist_count:905.9k plist_speed:297.4k/sec
REDUCE 20s [60.94%] edge_count:2.252M edge_speed:556.5k/sec plist_count:1.278M plist_speed:315.9k/sec
REDUCE 21s [93.21%] edge_count:3.444M edge_speed:681.5k/sec plist_count:1.555M plist_speed:307.7k/sec
REDUCE 22s [100.00%] edge_count:3.695M edge_speed:610.4k/sec plist_count:1.778M plist_speed:293.8k/sec
REDUCE 22s [100.00%] edge_count:3.695M edge_speed:584.4k/sec plist_count:1.778M plist_speed:281.3k/sec
Total: 22s
```

The output will be generated in the `out` directory by default. Here's the bulk
load output from the example above:

```sh
$ tree ./out
```

```txt
./out
├── 0
│   └── p
│       ├── 000000.vlog
│       ├── 000002.sst
│       └── MANIFEST
└── 1
    └── p
        ├── 000000.vlog
        ├── 000002.sst
        └── MANIFEST

4 directories, 6 files
```

Because `--reduce_shards` was set to `2`, two sets of `p` directories are generated: 
- the `./out/0` folder 
- the `./out/1` folder

Once the output is created, the files must be copied to all the servers that will run
Dgraph Alphas:

- Each replica of the first group (`Alpha1`, `Alpha2`, `Alpha3`) should have a copy of `./out/0/p`
- Each replica of the second group (`Alpha4`, `Alpha5`, `Alpha6`) should have a copy of `./out/1/p`, and so on.

{{% notice "note" %}}
Each Dgraph Alpha must have a copy of the group's `p` directory output. 
{{% /notice %}}

![Bulk Loader diagram](/images/deploy/bulk-loader.png)

### Other Bulk Loader options

You can further configure Bulk Loader using the following options:

- `--schema`, `-s`: set the location of the schema file.

- `--graphql_schema`, `-g` (optional): set the location of the GraphQL schema file.

- `--badger` superflag's `compression` option: Configure the compression of data
on disk. By default, the Snappy compression format is used, but you can also use
Zstandard compression. Or, you can choose no compression to minimize CPU usage. 
To learn more, see [Data Compression on Disk]({{< relref "/deploy/data-compression.md" >}}).

- `--new_uids`: (default: false): Assign new UIDs instead of using the existing
UIDs in data files. This is useful to avoid overriding the data in a DB already
in operation.

- `-f`, `--files`: Location of `*.rdf(.gz)` or `*.json(.gz)` file(s) to load. It can
load multiple files in a given path. If the path is a directory, then all files
ending in `.rdf`, `.rdf.gz`, `.json`, and `.json.gz` will be loaded.

- `--format` (optional): Specify file format (`rdf` or `json`) instead of getting it from
filenames. This is useful if you need to define a strict format manually.

- `--store_xids`: Generate a xid edge for each node. It will store the XIDs (The identifier / Blank-nodes) in an attribute named `xid` in the entity itself. It is useful if you gonna
use [External IDs]({{< relref "mutations/external-ids.md" >}}).

- `--xidmap` (default: `disabled`. Need a path): Store xid to uid mapping to a directory. Dgraph will save all identifiers used in the load for later use in other data ingest operations. The mapping will be saved in the path you provide and you must indicate that same path in the next load. It is recommended to use this flag if you have full control over your identifiers (Blank-nodes). Because the identifier will be mapped to a specific UID.

- `--vault` superflag (and its options): specify the Vault server address, role id, secret id, and
field that contains the encryption key required to decrypt the encrypted export.

## Load from S3

To bulk load from Amazon S3, you must have either [IAM](#iam-setup) or the following AWS credentials set
via environment variables:

 Environment Variable                        | Description
 --------------------                        | -----------
 `AWS_ACCESS_KEY_ID` or `AWS_ACCESS_KEY`     | AWS access key with permissions to write to the destination bucket.
 `AWS_SECRET_ACCESS_KEY` or `AWS_SECRET_KEY` | AWS access key with permissions to write to the destination bucket.

### IAM setup

In AWS, you can accomplish this by doing the following:
1. Create an [IAM Role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create.html) with an IAM Policy that grants access to the S3 bucket.
2. Depending on whether you want to grant access to an EC2 instance, or to a pod running on [EKS](https://aws.amazon.com/eks/), you can do one of these options:
   * [Instance Profile](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html) can pass the IAM Role to an EC2 Instance
   * [IAM Roles for Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html) to attach the IAM Role to a running EC2 Instance
   * [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) to associate the IAM Role to a [Kubernetes Service Account](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/).

Once your setup is ready, you can execute the bulk load from S3:

```sh
dgraph bulk -f s3:///bucket-name/directory-with-rdf -s s3:///bucket-name/directory-with-rdf/schema.txt
```

## Load from MinIO

To bulk load from MinIO, you must have the following MinIO credentials set via
environment variables:

 Environment Variable                        | Description
 --------------------                        | -----------
 `MINIO_ACCESS_KEY`                          | Minio access key with permissions to write to the destination bucket.
 `MINIO_SECRET_KEY`                          | Minio secret key with permissions to write to the destination bucket.


Once your setup is ready, you can execute the bulk load from MinIO:

```sh
dgraph bulk -f minio://minio-server:port/bucket-name/directory-with-rdf -s minio://minio-server:port/bucket-name/directory-with-rdf/schema.txt
```

## How to properly bulk load

Starting from Dgraph v20.03.7, v20.07.3 and v20.11.0 onwards, depending on your dataset size, you can follow one of the following ways to use bulk loader and initialize your new Cluster.

*The following procedure is particularly relevant for Clusters that have `--replicas` flag greater than 1*

### For small datasets

In case your dataset is small (a few GBs) it would be convenient to start by initializing just one Alpha node and then let the snapshot be streamed among the other Alpha replicas. You can follow these steps:
1. Run bulk loader only on one server
2. Once the `p` directory has been created by the bulk loader, then start **only** the first Alpha replica
3. Wait for 1 minute to ensure that a snapshot has been taken by the first Alpha node replica. You can confirm that a snapshot has been taken by looking for the following message":

```txt
I1227 13:12:24.202196   14691 draft.go:571] Creating snapshot at index: 30. ReadTs: 4.
```
4. After confirming that the snapshot has been taken, you can start the other Alpha node replicas (number of Alpha nodes must be equal to the `--replicas` flag value set in the zero nodes). Now the Alpha node (the one started in point 2) will be printing similar messages:

```txt
I1227 13:18:16.154674   16779 snapshot.go:246] Streaming done. Sent 1093470 entries. Waiting for ACK...
I1227 13:18:17.126494   16779 snapshot.go:251] Received ACK with done: true
I1227 13:18:17.126514   16779 snapshot.go:292] Stream snapshot: OK
```
These messages indicate that all replica nodes are now using the same snapshot. Thus, all your data is correctly in sync across the cluster. Also, the other alpha nodes will be printing (in their logs) something similar to:

```txt
I1227 13:18:17.126621    1720 draft.go:567] Skipping snapshot at 28, because found one at 28
```

### For bigger datasets

When your dataset is pretty big (e.g. dataset size > 10GB) it will be faster that you just copy the generated `p` directory (by the bulk loader) among all the Alphas nodes. You can follow these steps:

1. Run bulk loader only on one server
2. Copy (or use `rsync`) the `p` directory to the other servers (the servers you will be using to start the other Alpha nodes)
3. Now, start all Alpha nodes at the same time

If the process went well **all** Alpha nodes will take a snapshot after 1 minute. You will be seeing something similar to this in the Alpha logs:

```txt
I1227 13:27:53.959671   29781 draft.go:571] Creating snapshot at index: 34. ReadTs: 6.
```
Note that `snapshot at index` value must be the same within the same Alpha group and `ReadTs` must be the same value within and among all the Alpha groups.

### Using "p" directories coming from different Dgraph clusters

In some cases, you might want to use the `p` directory from an existing Dgraph cluster when creating a new cluster. You can do this by copying the `p` directory from your current Dgraph cluster into the new cluster, but you will need to perform an additional step before starting the Alpha nodes in the new cluster, as described below. 

After starting your Zero nodes, you need to increase the Zero's timestamp by sending the following `curl` request to the Zero leader node:

```
curl "zero_address:port/assign?what=timestamps&num=X" #with X = high number e.g. 100000 or higher
```
This will print the following message:

```
{"startId":"1","endId":"10000000","readOnly":"0"}
```
Now you need to confirm whether this timestamp has been increased as expected. You can do this by sending a `curl` request to the zero `/state` endpoint, as follows:

```
curl zero-address:port/state | jq
```
At the end of the response, look for the value shown for `"maxTxnTs"`. This value should be greater than or equal to the timestamp you assigned in the previous `curl` request, as shown in the following example:

```json
  "maxLeaseId": "0",
  "maxTxnTs": "10010000",
  "maxRaftId": "0",
  "removed": [],
  "cid": "47285b0d-6223-421e-aab5-e6910620a8ed",
  "license": {
    "user": "",
    "maxNodes": "18446744073709551615",
    "expiryTs": "1619041648",
    "enabled": true
  }
```
Now, start your Alpha nodes and check that the Snapshot created has a `ReadTs` value that's greater than or equal to the `"maxTxnTs"` value you viewed in the previous step.

```
I0322 14:52:40.858626 2885131 draft.go:606] Creating snapshot at Index: 180, ReadTs: 10000011
```

## Enterprise Features

### Multi-tenancy (Enterprise Feature)

By default, Bulk loader preserves the namespace in the data and schema files.
If there's no namespace information available, it loads the data into the default namespace.

Using the `--force-namespace` flag, you can load all the data into a specific namespace.
In that case, the namespace information from the data and schema files will be ignored.

For example, to force the bulk data loading into namespace `123`:

```sh
dgraph bulk -s /tmp/data/1million.schema -f /tmp/data/1million.rdf.gz --force-namespace 123
```

### Encryption at rest (Enterprise Feature)

Even before the Dgraph cluster starts, we can load data using Bulk Loader with the encryption feature turned on. Later we can point the generated `p` directory to a new Alpha server.

Here's an example to run Bulk Loader with a key used to write encrypted data:

```bash
dgraph bulk --encryption key-file=./enc_key_file -f data.json.gz -s data.schema --map_shards=1 --reduce_shards=1 --http localhost:8000 --zero=localhost:5080
```
Alternatively, starting with v20.07.0, the `vault_*` options can be used to decrypt the encrypted export.


### Encrypting imports (Enterprise Feature)

The Bulk Loader’s `--encryption key-file=value` option was previously used to encrypt the output `p` directory. This same option will also be used to decrypt the encrypted export data and schema files.

Another option, `--encrypted`, indicates whether the input `rdf`/`json` data and schema files are encrypted or not. With this switch, we support the use case of migrating data from unencrypted exports to encrypted import.

So, with the above two options we have 4 cases:

1. `--encrypted=true` and no `encryption key-file=value`.

Error: If the input is encrypted, a key file must be provided.

2. `--encrypted=true` and `encryption key-file=path-to-key`.

Input is encrypted and output `p` dir is encrypted as well.

3. `--encrypted=false` and no `encryption key-file=value`.

Input is not encrypted and the output `p` dir is also not encrypted.   

4. `--encrypted=false` and `encryption key-file=path-to-key`.

Input is not encrypted but the output is encrypted. (This is the migration use case mentioned above).

Alternatively, starting with v20.07.0, the `vault_*` options can be used instead of the `--encryption key-file=value` option above to achieve the same effect except that the keys are sitting in a Vault server.

## Tuning & monitoring

### Performance Tuning

{{% notice "tip" %}}
We highly recommend [disabling swap
space](https://askubuntu.com/questions/214805/how-do-i-disable-swap) when
running Bulk Loader. It is better to fix the parameters to decrease memory
usage, than to have swapping grind the loader down to a halt.
{{% /notice %}}

Flags can be used to control the behavior and performance characteristics of
the bulk loader. You can see the full list by running `dgraph bulk --help`. In
particular, **you should tune the flags so that Bulk Loader doesn't use more
memory than is available as RAM**. If it starts swapping, it will become
incredibly slow.

**In the map phase**, tweaking the following flags can reduce memory usage:

- The `--num_go_routines` flag controls the number of worker threads. Lowering reduces memory
  consumption.

- The `--mapoutput_mb` flag controls the size of the map output files. Lowering
  reduces memory consumption.

For bigger datasets and machines with many cores, gzip decoding can be a
bottleneck during the map phase. Performance improvements can be obtained by
first splitting the RDFs up into many `.rdf.gz` files (e.g. 256MB each). This
has a negligible impact on memory usage.

**The reduce phase** is less memory heavy than the map phase, although can still
use a lot.  Some flags may be increased to improve performance, *but only if
you have large amounts of RAM*:

- The `--reduce_shards` flag controls the number of resultant Dgraph alpha instances.
  Increasing this increases memory consumption, but in exchange allows for
higher CPU utilization.

- The `--map_shards` flag controls the number of separate map output shards.
  Increasing this increases memory consumption but balances the resultant
Dgraph alpha instances more evenly.
