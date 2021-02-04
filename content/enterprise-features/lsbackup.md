+++
date = "2017-03-20T22:25:17+11:00"
title = "Backup list tool"
weight = 4
[menu.main]
    parent = "enterprise-features"
+++

`lsbackup` looks at a location where backups are stored and prints information about them.

Here we have only two flags that is the --location flag that indicates a source URI with Dgraph backup objects. This URI supports all the schemes used for backup.

The other flag is the --verbose flag that if enabled will print additional information about the backup.

```txt
Flags:
  -h, --help              help for lsbackup
  -l, --location string   Sets the source location URI (required).
      --verbose           Outputs additional info in backup list.
```
How to run the command:

The lsbackup command is easy to run as follows:
```sh
dgraph lsbackup -l <source-location-URI>
```
Below are the Source URI format and parts

Source URI formats:

```txt
[scheme]://[host]/[path]?[args]
[scheme]:///[path]?[args]
/[path]?[args] (only for local or NFS)
```

Source URI parts:

- `scheme` - service handler, one of: `s3`, `minio`, `file`
- `host` - remote address. ex: `dgraph.s3.amazonaws.com`
- `path` - directory, bucket or container at target. ex: `/dgraph/backups/`
- `args` - specific arguments that are ok to appear in logs.

Examples:

### S3

checking information about backups stored in an AWS S3 bucket

```sh
dgraph lsbackup -l s3:///s3.us-west-2.amazonaws.com/dgraph_backup
```

You might need to set up access and secret key env variable in the shell (or session) you are going to run lsbackup command. This can be done this was:
```
AWS_SECRET_ACCESS_KEY=<paste-your-secret-access-key>
AWS_ACCESS_ID=<paste-your-key-id>
```

### MinIO

checking information about backups stored in a Minio bucket:

```sh
dgraph lsbackup -l minio://localhost:9000/dgraph_backup
```

In case Minio server is started without tls, one has to specify explicitly that secure=false as it set to true by default. Also one has to set the environment variable for the access key and secret key. 

So in order to get the lsbackup running one has to do the following steps:

set MINIO_ACCESS_KEY as an environment variable for the running shell this can be done with the following command export MINIO_ACCESS_KEY=minioadmin (minioadmin is the default access key, unless is changed by the user)

set MINIO_SECRET_KEY as an environment variable for the running shell this can be done with the following command export MINIO_SECRET_KEY=minioadmin (minioadmin is the default secret key, unless is changed by the user)

add the argument secure=false to the lsbackup command, that means the command will look like: dgraph lsbackup -l "minio://localhost:9000/<bucket-name>?secure=false" (not the double quotes (”) are required.

Local: checking information about backups stored locally (on disk):

```sh
dgraph lsbackup -l ~/dgraph_backup
```

Output (what is printing this command):

The output of this command is the following:

```txt
[Decoder]: Using assembly version of decoder
Page Size: 4096
Listing backups from: ~/backup
Name	Since	Groups	Encrypted
dgraph_backup/dgraph.20210121.125014.852/manifest.json	30005	map[1:[dgraph.graphql.schema_created_at dgraph.graphql.xid dgraph.drop.op dgraph.type dgraph.cors dgraph.graphql.schema_history score dgraph.graphql.p_query dgraph.graphql.schema dgraph.graphql.p_sha256hash series]]	false
```

I admit I don't like how we are printing the output as of now therefore I’ve sent this PR1 and PR2 that changes the output to the following one: (note PR2 will remove the first 2 lines, the ones reporting [Decoder]: Using … and Page Size: 4096 in order to provide better formatting experience for the user (e.g. using jq )

```json
[
	{
		"path": "/home/user/Dgraph/20.11/backup/dgraph.20210121.125014.852/manifest.json",
		"since": 30005,
		"backup_id": "reverent_vaughan0",
		"backup_num": 1,
		"encrypted": false,
		"type": "full"
	},
]
```


We’ve also added/changed a few things:

changed wording from Name → path

Added DropOperations section 

Added Type as well to the output that will tell if the backup is full or incremental one

Added backup_id and backup_num

`--verbose` flag: if enabled this will print additional information about Groups and DropOperations

If `--verbose` flag is enabled an example of the output would look like this:

```json
[
    {
        "path": "/home/user/Dgraph/20.11/bkp/dgraph.20210121.125014.852/manifest.json",
        "since": 30005,
        "backup_id": "reverent_vaughan0",
        "backup_num": 1,
        "encrypted": false,
        "type": "full",
        "groups": {
            "1": [
                "dgraph.graphql.schema_created_at",
                "dgraph.graphql.xid",
                "dgraph.drop.op",
                "dgraph.type",
                "dgraph.cors",
                "dgraph.graphql.schema_history",
                "score",
                "dgraph.graphql.p_query",
                "dgraph.graphql.schema",
                "dgraph.graphql.p_sha256hash",
                "series"
            ]
        }
    },
]
```

It’s only merged master and it will be part of 21.03 in order to avoid breaking changes in 20.11. For 20.11, 20.07 and 20.03 the output will not change.

In the table below I’m explaining what does each term/section means (when documenting them please follow the same order as they are printed in the above output command):

- `path`: Name of the backup

- `since`:  is the timestamp at which this backup was taken. It's called Since because it will become the timestamp from which to backup in the next   incremental backup.

- `groups`: is the map of valid groups to predicates at the time the backup was created. This is printed only if `--verbose` flag is enabled

- `encrypted`: Indicates whether this backup is encrypted or not

- `type`: Indicates whether this backup is a full or incremental one

- `drop_operation`: lists the various DROP operations that took place since the last backup.  These are used during restore to redo those operations before applying the backup. (This is printed only if `--verbose` flag is enabled)

- `backup_num`: is a monotonically increasing number assigned to each backup in  a series. The full backup as BackupNum equal to one and each incremental  backup gets assigned the next available number. This can be used to verify the integrity of the data during a restore.

- `backup_id`: is a unique ID assigned to all the backups in the same series.

