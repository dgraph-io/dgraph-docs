+++
title = "Data migration"
keywords = "Data, migration, csv, sql,"
[menu.main]
    parent = "migration"
    weight = 1
+++

To load CSV-formatted data or SQL data into Dgraph,
first convert the dataset into one of the accepted formats ([RDF N-Quad/Triple](https://www.w3.org/TR/n-quads/) or JSON) and then load the
resulting dataset into Dgraph.

After you convert the `.csv` or `.sql` files to [RDF N-Quad/Triple](https://www.w3.org/TR/n-quads/) or JSON, 
you can use [Dgraph Live Loader]({{< relref "/deploy/fast-data-loading/live-loader.md" >}}) or 
[Dgraph Bulk Loader]({{< relref "/deploy/fast-data-loading/bulk-loader.md" >}}) to import your data.



