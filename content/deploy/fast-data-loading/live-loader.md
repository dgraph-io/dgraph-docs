+++
date = "2017-03-20T22:25:17+11:00"
title = "Live Loader"
weight = 12
[menu.main]
    parent = "fast-data-loading"
+++

Dgraph Live Loader (run with `dgraph live`) is a small helper program which reads RDF N-Quads from a gzipped file, batches them up, creates mutations (using the go client) and shoots off to Dgraph.

Dgraph Live Loader correctly handles assigning unique IDs to blank nodes across multiple files, and can optionally persist them to disk to save memory, in case the loader was re-run.

{{% notice "note" %}} Dgraph Live Loader can optionally write the `xid`->`uid` mapping to a directory specified using the `--xidmap` flag, which can reused
given that live loader completed successfully in the previous run.{{% /notice %}}

{{% notice "note" %}} Live Loader only accept [RDF N-Quad/Triple
data](https://www.w3.org/TR/n-quads/) or JSON in plain or gzipped format. Data
in other formats must be converted.{{% /notice %}}

```sh
dgraph live --help # To see the available flags.

# Read RDFs or JSON from the passed file, and send them to Dgraph on localhost:9080.
dgraph live --files <path-to-gzipped-RDF-or-JSON-file>

# Read multiple RDFs or JSON from the passed path, and send them to Dgraph on localhost:9080.
dgraph live --files <./path-to-gzipped-RDF-or-JSON-files>

# Read multiple files strictly by name.
dgraph live --files <file1.rdf, file2.rdf>

# Use compressed gRPC connections to and from Dgraph.
dgraph live --use_compression --files <path-to-gzipped-RDF-or-JSON-file>

# Read RDFs and a schema file and send to Dgraph running at given address.
dgraph live \
  --files <path-to-gzipped-RDf-or-JSON-file> \
  --schema <path-to-schema-file> \
  --alpha <dgraph-alpha-address:grpc_port> \
  --zero <dgraph-zero-address:grpc_port>
```

## Load from S3

To live load from [Amazon S3 (Simple Storage Service)](https://aws.amazon.com/s3/), you must have either permissions to access the S3 bucket from the system performing live load (see [IAM setup](#iam-setup) below) or explicitly add the following AWS credentials set via environment variables:

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

Once your setup is ready, you can execute the live load from S3.  As examples:

```sh
## short form of S3 URL
dgraph live \
  --files s3:///<bucket-name>/<directory-with-data-files> \
  --schema s3:///<bucket-name>/<directory-with-data-files>/schema.txt

## long form of S3 URL
dgraph live \
  --files s3://s3.<region>.amazonaws.com/<bucket>/<directory-with-data-files> \
  --schema s3://s3.<region>.amazonaws.com/<bucket>/<directory-with-data-files>/schema.txt
```

{{% notice "note" %}}
The short form of the S3 URL requires S3 URL is prefixed with `s3:///` (noticed the triple-slash `///`).  The long form for S3 buckets requires a double slash, e.g. `s3://`.
{{% /notice %}}


## Load from MinIO

To live load from MinIO, you must have the following MinIO credentials set via
environment variables:

 Environment Variable                        | Description
 --------------------                        | -----------
 `MINIO_ACCESS_KEY`                          | Minio access key with permissions to write to the destination bucket.
 `MINIO_SECRET_KEY`                          | Minio secret key with permissions to write to the destination bucket.


Once your setup is ready, you can execute the bulk load from MinIO:

```sh
dgraph live \
  --files minio://minio-server:port/<bucket-name>/<directory-with-data-files> \
  --schema minio://minio-server:port/<bucket-name>/<directory-with-data-files>/schema.txt
```

## Enterprise Features

### Multi-tenancy (Enterprise Feature)

Since [multi-tenancy]({{< relref "multitenancy.md" >}}) requires ACL,
when using the Live loader you must provide the login credentials using the `--creds` flag.
By default, Live loader loads the data into the user's namespace.

[Guardians of the Galaxy]({{< relref "multitenancy.md#guardians-of-the-galaxy" >}}) can load the data into multiple namespaces.
Using `--force-namespace`, a _Guardian_ can load the data into the namespace specified in the data and schema files.

{{% notice "note" %}}
The Live loader requires that the `namespace` from the data and schema files exist before loading the data.
{{% /notice %}}

For example, to preserve the namespace while loading data first you need to create the namespace(s) and then run the live loader command:

```sh
dgraph live \
  --schema /tmp/data/1million.schema \
  --files /tmp/data/1million.rdf.gz --creds="user=groot;password=password;namespace=0" \
  --force-namespace -1
```

A _Guardian of the Galaxy_ can also load data into a specific namespace. For example, to force the data loading into namespace `123`:

```sh
dgraph live \
  --schema /tmp/data/1million.schema \
  --files /tmp/data/1million.rdf.gz \
  --creds="user=groot;password=password;namespace=0" \
  --force-namespace 123
```

### Encrypted imports (Enterprise Feature)

A new flag `--encryption key-file=value` is added to the Live Loader. This option is required to decrypt the encrypted export data and schema files. Once the export files are decrypted, the Live Loader streams the data to a live Alpha instance.
Alternatively, starting with v20.07.0, the `vault_*` options can be used to decrypt the encrypted export and schema files.

{{% notice "note" %}}
If the live Alpha instance has encryption turned on, the `p` directory will be encrypted. Otherwise, the `p` directory is unencrypted.
{{% /notice %}}

For example, to load an encrypted RDF/JSON file and schema via Live Loader:

```sh
dgraph live \
 --files <path-containering-encrypted-data-files> \
 --schema <path-to-encrypted-schema> \
 --encryption key-file=<path-to-keyfile-to-decrypt-files>
```

## Batch upserts

With batch upserts in Live Loader, you can insert big data-sets (multiple files) into an existing cluster that might contain nodes that already exist in the graph.
Live Loader generates an `upsertPredicate` query for each of the ids found in the request, while
adding the corresponding `xid` to that `uid`. The added mutation is only useful if the `uid` doesn't exists.

The `-U, --upsertPredicate` flag runs the Live Loader in "upsert predicate" mode. The provided predicate needs to be indexed, and the Loader will use it to store blank nodes as a `xid`.

{{% notice "note" %}}
When the `upsertPredicate` already exists in the data, the existing node with this `xid` is modified and no new node is added.
{{% /notice %}}

For example:
```sh
dgraph live --files <directory-with-data-files> --schema <path-to-schema-file> --upsertPredicate <xid>
```

## Other Live Loader options

`--new_uids` (default: `false`): Assign new UIDs instead of using the existing
UIDs in data files. This is useful to avoid overriding the data in a DB already
in operation.

`-f, --files`: Location of *.rdf(.gz) or *.json(.gz) file(s) to load. It can
load multiple files in a given path. If the path is a directory, then all files
ending in .rdf, .rdf.gz, .json, and .json.gz will be loaded.

`--format`: Specify file format (`rdf` or `json`) instead of getting it from
filenames. This is useful if you need to define a strict format manually.

`-b, --batch` (default: `1000`): Number of N-Quads to send as part of a mutation.

`-c, --conc` (default: `10`): Number of concurrent requests to make to Dgraph.
Do not confuse with `-C`.

`-C, --use_compression` (default: `false`): Enable compression for connections to and from the
Alpha server.

`-a, --alpha` (default: `localhost:9080`): Dgraph Alpha gRPC server address to connect for live loading. This can be a comma-separated list of Alphas addresses in the same cluster to distribute the load, e.g.,  `"alpha:grpc_port,alpha2:grpc_port,alpha3:grpc_port"`.

`-x, --xidmap` (default: disabled. Need a path): Store `xid` to `uid` mapping to a directory. Dgraph will save all identifiers used in the load for later use in other data ingest operations. The mapping will be saved in the path you provide and you must indicate that same path in the next load.

{{% notice "tip" %}}
Using the `--xidmap` flag is recommended if you have full control over your identifiers (Blank-nodes). Because the identifier will be mapped to a specific `uid`.
{{% /notice %}}

The `--ludicrous` superflag's `enabled` option (default: `false`): This option allows the user to notify Live Loader that the Alpha server is running in ludicrous mode.
Live Loader, by default, does smart batching of data to avoid transaction conflicts, which improves the performance in normal mode.
Since there's no conflict detection in Ludicrous mode, smart batching is disabled to speed up data ingestion.

{{% notice "note" %}}
You should only use the `--ludicrous` superflag's `enabled` option if Dgraph is also running in [ludicrous mode]({{< relref "ludicrous-mode.md" >}}).
{{% /notice %}}

`-U, --upsertPredicate` (default: disabled): Runs Live Loader in `upsertPredicate` mode. The provided value will be used to store blank nodes as a `xid`.

`--vault` [superflag's]({{< relref "deploy/cli-command-reference" >}}) options specify the Vault server address, role id, secret id, and
field that contains the encryption key required to decrypt the encrypted export.

## `upsertPredicate` example

You might find that discrete pieces of information regarding entities are arriving through independent data feeds.
The feeds might involve adding basic information (first and last name), income, and address in separate files.
You can use the live loader to correlate individual records from these files and combine attributes to create a consolidated Dgraph node.

Start by adding the following schema:

```
<address>: [uid] @reverse .
<annualIncome>: float .
<city>: string @index(exact) .
<firstName>: string @index(exact) .
<lastName>: string @index(exact) .
<street>: string @index(exact) .
<xid>: string @index(hash) .
```

### The Upsert predicate

You can upload the files individually using the live loader (`dgraph live`) with the `-U` or `--upsertPredicate` option.
Each file has records with external keys for customers (e.g., `my.org/customer/1`) and addresses (e.g., `my.org/customer/1/address/1`).

The schema has the required fields in addition to a field named `xid`. This field will be used to hold the external key value. Please note that there's a `hash` index for the `xid` field. You will be using this `xid` field as the "Upsert" predicate (`-U` option) and pass it as an argument to the `dgraph live` command. The live loader uses the predicate's content provided by the `-U` option (`xid` in this case) to identify and update the corresponding Dgraph node. In case the corresponding Dgraph node does not exist, the live loader will create a new node.

**File** `customerNames.rdf` - Basic information like customer's first and last name:

```
<_:my.org/customer/1>       <firstName>  "John"     .
<_:my.org/customer/1>       <lastName>  "Doe"     .
<_:my.org/customer/2>       <firstName>  "James"     .
<_:my.org/customer/2>       <lastName>  "Doe"     .
```

You can load the customer information with the following command:

```sh
dgraph live --files customerNames.rdf --upsertPredicate "xid"
```

Next, you can inspect the loaded data:  

```graphql
{
  q1(func: has(firstName)){
    uid
    firstName
    lastName
    annualIncome
    xid
    address{
      uid
      street
      xid
    }
  }  
}
```

The query will return the newly created Dgraph nodes as shown below.

```json
"q1": [
  {
    "uid": "0x14689d2",
    "firstName": "John",
    "lastName": "Doe",
    "xid": "my.org/customer/1"
  },
  {
    "uid": "0x14689d3",
    "firstName": "James",
    "lastName": "Doe",
    "xid": "my.org/customer/2"
  }
]
```

You can see the new customer added with name information and the contents of the `xid` field.
The `xid` field holds a reference to the externally provided id.

**File** `customer_income.rdf` - Income information about the customer:

```
<_:my.org/customer/1>       <annualIncome> "90000"    .
<_:my.org/customer/2>       <annualIncome> "75000"    .
```

You can load the income information by running:

```sh
dgraph live --files customer_income.rdf --upsertPredicate "xid"
```

Now you can execute a query to check the income data:

```graphql
{
  q1(func: has(firstName)){
    uid
    firstName
    lastName
    annualIncome
    xid
    address{
      uid
      street
      city
      xid
    }
  }  
}
```

Note that the corresponding nodes have been correctly updated with the `annualIncome` attribute.

```json
"q1": [
  {
    "uid": "0x14689d2",
    "firstName": "John",
    "lastName": "Doe",
    "annualIncome": 90000,
    "xid": "my.org/customer/1"
  },
  {
    "uid": "0x14689d3",
    "firstName": "James",
    "lastName": "Doe",
    "annualIncome": 75000,
    "xid": "my.org/customer/2"
  }
]   
```

**File** `customer_address.rdf` - Address information:

```
<_:my.org/customer/1>     <address> <_:my.org/customer/1/address/1>    .
<_:my.org/customer/1/address/1>  <street> "One High Street" .
<_:my.org/customer/1/address/1>  <city> "London" .
<_:my.org/customer/2>        <address> <_:my.org/customer/2/address/1>   .
<_:my.org/customer/2/address/1>  <street> "Two Main Street" .
<_:my.org/customer/2/address/1>  <city> "New York" .
<_:my.org/customer/2>     <address> <_:my.org/customer/2/address/2>   .
<_:my.org/customer/2/address/2>  <street> "Ten Main Street" .
<_:my.org/customer/2/address/2>  <city> "Mumbai" .
```

You can extend the same approach to update `uid` predicates.
To load the addresses linked to customers, you can launch the live loader as below.

```sh
dgraph live --files customer_address.rdf --upsertPredicate "xid"
```

You can check the output of the query:

```graphql
{
  q1(func: has(firstName)){
    uid
    firstName
    lastName
    annualIncome
    xid
    address{
      uid
      street
      xid
    }
  }
}
```

The addresses are correctly added as a `uid` predicate in the respective customer nodes.

```json
"q1": [
  {
    "uid": "0x14689d2",
    "firstName": "John",
    "lastName": "Doe",
    "annualIncome": 90000,
    "xid": "my.org/customer/1",
    "address": [
      {
        "uid": "0x1945bb6",
        "street": "One High Street",
        "city": "London",
        "xid": "my.org/customer/1/address/1"
      }
    ]
  },
  {
    "uid": "0x14689d3",
    "firstName": "James",
    "lastName": "Doe",
    "annualIncome": 75000,
    "xid": "my.org/customer/2",
    "address": [
      {
        "uid": "0x1945bb4",
        "street": "Two Main Street",
        "city": "New York",
        "xid": "my.org/customer/2/address/1"
      },
      {
        "uid": "0x1945bb5",
        "street": "Ten Main Street",
        "city": "Mumbai",
        "xid": "my.org/customer/2/address/2"
      }
    ]
  }
]
```
