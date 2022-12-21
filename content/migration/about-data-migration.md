+++
title = "Data migration"
keywords = "Data, migration, csv, sql,"
[menu.main]
    parent = "migration"
    weight = 1
+++

[Dgraph mutations]({{< relref "mutations/_index.md" >}}) are accepted in RDF
N-Quad and JSON formats. To load CSV-formatted data or SQL data into Dgraph,
first convert the dataset into one of the accepted formats and then load the
resulting dataset into Dgraph.

After you converte the `.csv` or `.sql` files to [RDF N-Quad/Triple](https://www.w3.org/TR/n-quads/) or JSON, 
you can use [Dgraph Live Loader]({{< relref "/deploy/fast-data-loading/live-loader.md" >}}) or 
[Dgraph Bulk Loader]({{< relref "/deploy/fast-data-loading/bulk-loader.md" >}}) to import your data.

To convert the `.csv` file you can use any CSV to JSON conversion tool. However, to covert SQL to JSON use the Dgraph migration tool.


## Command-line options

You can run the Dgraph migrate tool using this command:

```sh
dgraph migrate [flags]
```

| Flag | Description| 
|---------:|:---------|
| --db string | The database to import|
| -h, --help | help for migrate |
| --host string | The hostname or IP address of the database server. The default is "localhost"|
| -o, --output_data string | The data output file (default "sql.rdf") |
| -s, --output_schema string | The schema output file (default "schema.txt") |
| --password string | The password used for logging in |
| --port string | The port of the database server. (default "3306")|
| -q, --quiet | Enable quiet mode to suppress the warning logs|
| -p, --separator string | The separator for constructing predicate names (default ".")|
| --tables string| The comma separated list of tables to import, an empty string means importing all tables in the database|
| --user string | The user for logging in |


