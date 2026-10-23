---
title: Import Data
---

As an `Administrator` you can initialize a new Dgraph cluster by doing an [Initial import](bulk-loader) and you can import data into a running instance by performing a [Live import](live-loader).


Initial import is **considerably faster** than the live import but can only be used to load data into a new cluster (without prior data) and is executed before starting the Alpha nodes.


:::note
Both options accept [RDF N-Quad/Triple
data](https://www.w3.org/TR/n-quads/) or JSON format. Refers to [data migration](import-data) to see how to convert other data formats.
:::


To load CSV-formatted data or SQL data into Dgraph,
first convert the dataset into one of the accepted formats ([RDF N-Quad/Triple](https://www.w3.org/TR/n-quads/) or JSON) and then load the
resulting dataset into Dgraph.

After you convert the `.csv` or `.sql` files to [RDF N-Quad/Triple](https://www.w3.org/TR/n-quads/) or JSON,
you can use [Dgraph Live Loader](live-loader) or
[Dgraph Bulk Loader](bulk-loader) to import your data.
