+++
date = "2017-03-20T22:25:17+11:00"
title = "Backup List Tool"
weight = 3
[menu.main]
    parent = "enterprise-features"
+++

The `lsbackup` command-line tool prints information about the stored backups in a user-defined location.

## Parameters

The `lsbackup` command has two flags:

```txt
Flags:
  -h, --help              help for lsbackup
  -l, --location string   Sets the source location URI (required).
      --verbose           Outputs additional info in backup list.
```

- `--location`: indicates a [source URI](#source-uri) with Dgraph backup objects. This URI supports all the schemes used for backup.
- `--verbose`: if enabled will print additional information about the selected backup.

For example, you can execute the `lsbackup` command as follows:

```sh
dgraph lsbackup -l <source-location-URI>
```

### Source URI

Source URI formats:

- `[scheme]://[host]/[path]?[args]`
- `[scheme]:///[path]?[args]`
- `/[path]?[args]` (only for local or NFS)

Source URI parts:

- `scheme`: service handler, one of: `s3`, `minio`, `file`
- `host`: remote address; e.g.: `dgraph.s3.amazonaws.com`
- `path`: directory, bucket or container at target; e.g.: `/dgraph/backups/`
- `args`: specific arguments that are ok to appear in logs

## Output

The following snippet is an example output of `lsbackup`:

```json
[
	{
		"path": "/home/user/Dgraph/20.11/backup/manifest.json",
		"since": 30005,
		"backup_id": "reverent_vaughan0",
		"backup_num": 1,
		"encrypted": false,
		"type": "full"
	},
]
```

If the `--verbose` flag was enabled, the output would look like this:

```json
[
    {
        "path": "/home/user/Dgraph/20.11/backup/manifest.json",
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

### Return values

- `path`: Name of the backup

- `since`:  is the timestamp at which this backup was taken. It's called Since because it will become the timestamp from which to backup in the next   incremental backup.

- `groups`: is the map of valid groups to predicates at the time the backup was created. This is printed only if `--verbose` flag is enabled

- `encrypted`: Indicates whether this backup is encrypted or not

- `type`: Indicates whether this backup is a full or incremental one

- `drop_operation`: lists the various DROP operations that took place since the last backup.  These are used during restore to redo those operations before applying the backup. (This is printed only if `--verbose` flag is enabled)

- `backup_num`: is a monotonically increasing number assigned to each backup in  a series. The full backup as BackupNum equal to one and each incremental  backup gets assigned the next available number. This can be used to verify the integrity of the data during a restore.

- `backup_id`: is a unique ID assigned to all the backups in the same series.


## Examples

### S3

Checking information about backups stored in an AWS S3 bucket:

```sh
dgraph lsbackup -l s3:///s3.us-west-2.amazonaws.com/dgraph_backup
```

You might need to set up access and secret key environment variables in the shell (or session) you are going to run the `lsbackup` command. For example:
```
AWS_SECRET_ACCESS_KEY=<paste-your-secret-access-key>
AWS_ACCESS_ID=<paste-your-key-id>
```

### MinIO

Checking information about backups stored in a MinIO bucket:

```sh
dgraph lsbackup -l minio://localhost:9000/dgraph_backup
```

In case the MinIO server is started without `tls`, you must specify that `secure=false` as it set to `true` by default. You also need to set the environment variables for the access key and secret key. 

In order to get the `lsbackup` running, you should following these steps:

- Set `MINIO_ACCESS_KEY` as an environment variable for the running shell this can be done with the following command:
  (`minioadmin` is the default access key, unless is changed by the user)

  ```
  export MINIO_ACCESS_KEY=minioadmin
  ```

- Set MINIO_SECRET_KEY as an environment variable for the running shell this can be done with the following command:
  (`minioadmin` is the default secret key, unless is changed by the user)

  ```
  export MINIO_SECRET_KEY=minioadmin
  ```

- Add the argument `secure=false` to the `lsbackup command`, that means the command will look like: (the double quotes `"` are required)

  ```sh
  dgraph lsbackup -l "minio://localhost:9000/<bucket-name>?secure=false"
  ```

### Local

Checking information about backups stored locally (on disk):

```sh
dgraph lsbackup -l ~/dgraph_backup
```
