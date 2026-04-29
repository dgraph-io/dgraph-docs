---
title: Backup List Tool
---

The `lsbackup` command-line tool prints information about the stored backups in a user-defined location.

## Parameters

The `lsbackup` command supports the following flags:

```txt
Flags:
  -h, --help                    help for lsbackup
  -l, --location string         Sets the source location URI (required).
      --verbose                 Outputs additional info in backup list.
      --since-date string       Only list backups taken on or after this date (YYYY-MM-DD or RFC 3339).
      --until-date string       Only list backups taken on or before this date (YYYY-MM-DD or RFC 3339).
      --last-n-days int         Only list backups from the last N calendar days. Cannot be combined with --since-date.
      --summary                 Print a summary block after the backup listing.
```

- `--location`: indicates a [source URI](#source-uri) with Dgraph backup objects. This URI supports all the schemes used for backup.
- `--verbose`: if enabled will print additional information about the selected backup, including predicate groups and DROP operations. Reads the full `manifest.json` instead of the lightweight summary.
- `--since-date`: filters results to backups taken on or after the given date. Accepts `YYYY-MM-DD` (interpreted as start of that day UTC) or RFC 3339 (e.g. `2024-06-15T08:00:00Z`).
- `--until-date`: filters results to backups taken on or before the given date. Accepts `YYYY-MM-DD` (interpreted as end of that day UTC, i.e. 23:59:59.999) or RFC 3339.
- `--last-n-days`: shorthand for `--since-date` set to N calendar days ago at midnight UTC. Cannot be combined with `--since-date`.
- `--summary`: prints a human-readable summary block to stderr after the JSON output (total count, oldest/newest backup, last full/incremental).

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


## Date Filtering

Both `--since-date` / `--until-date` and `--last-n-days` can be used to narrow results to a specific time window.

- `YYYY-MM-DD` dates are **inclusive**: `--until-date 2024-06-15` captures all backups taken any time on 15 June.
- `--last-n-days 7` is equivalent to setting `--since-date` to 7 days ago at midnight UTC.
- `--last-n-days` and `--since-date` are mutually exclusive.

```sh
# Last 7 days
dgraph lsbackup -l /data/backups --last-n-days 7

# A specific month with a summary
dgraph lsbackup -l /data/backups --since-date 2024-03-01 --until-date 2024-03-31 --summary

# Backups before a specific incident time
dgraph lsbackup -l /data/backups --until-date "2024-06-15T13:59:59Z"
```

## Performance Note

By default, `lsbackup` reads `manifest_summary.json` — a lightweight file that omits predicate groups and DROP operations. On clusters with large vector schemas, `manifest.json` can exceed 500 MB; the summary keeps listing fast regardless of cluster size.

Use `--verbose` only when you need predicate-level detail, such as when diagnosing a restore or auditing schema changes.

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
