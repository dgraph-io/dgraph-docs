---
title: dgraph conv
---

#### `dgraph conv`

This command runs the Dgraph geographic file converter, which converts geographic
files into RDF so that they can be consumed by Dgraph. The following replicates
the help listing shown when you run `dgraph conv --help`:

```shell
Dgraph Geo file converter
Usage:
 dgraph conv [flags]

Flags:
     --geo string       Location of geo file to convert
     --geopred string   Predicate to use to store geometries (default "loc")
 -h, --help             help for conv
     --out string       Location of output rdf.gz file (default "output.rdf.gz")

Use "dgraph conv [command] --help" for more information about a command.
```


