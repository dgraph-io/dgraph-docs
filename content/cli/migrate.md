+++
title = "dgraph migrate"
weight = 3
type = "docs"
[menu.main]
    parent = "cli"
+++


#### `dgraph migrate`

This command runs the Dgraph [migration tool]({{< relref "migration/migrate-tool.md" >}})
to move data from a MySQL database to Dgraph. The following replicates the help
listing shown when you run `dgraph migrate --help`:

```shell
Run the Dgraph migration tool from a MySQL database to Dgraph
Usage:
 dgraph migrate [flags]

Flags:
     --db string              The database to import
 -h, --help                   help for migrate
     --host string            The hostname or IP address of the database server. (default "localhost")
 -o, --output_data string     The data output file (default "sql.rdf")
 -s, --output_schema string   The schema output file (default "schema.txt")
     --password string        The password used for logging in
     --port string            The port of the database server. (default "3306")
 -q, --quiet                  Enable quiet mode to suppress the warning logs
 -p, --separator string       The separator for constructing predicate names (default ".")
     --tables string          The comma separated list of tables to import, an empty string means importing all tables in the database
     --user string            The user for logging in

Use "dgraph migrate [command] --help" for more information about a command.
```

#### `dgraph upgrade`

This command helps you to upgrade from an earlier Dgraph release to a newer release.
The following replicates the help listing shown when you run `dgraph upgrade --help`:

```shell
This tool is supported only for the mainstream release versions of Dgraph, not for the beta releases.
Usage:
 dgraph upgrade [flags]

Flags:
     --acl               upgrade ACL from v1.2.2 to >=v20.03.0
 -a, --alpha string      Dgraph Alpha gRPC server address (default "127.0.0.1:9080")
 -d, --deleteOld         Delete the older ACL types/predicates (default true)
     --dry-run           dry-run the upgrade
 -f, --from string       The version string from which to upgrade, e.g.: v1.2.2
 -h, --help              help for upgrade
 -p, --password string   Password of ACL user
 -t, --to string         The version string till which to upgrade, e.g.: v20.03.0
 -u, --user string       Username of ACL user

Use "dgraph upgrade [command] --help" for more information about a command.
```
