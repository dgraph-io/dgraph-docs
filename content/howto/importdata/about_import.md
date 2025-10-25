+++
title = "Import data"
type = "docs"
keywords = "import data, howto, task"
[menu.main]
    parent = "importdata"
    weight = 1
+++

As an `Administrator` you can initialize a new Dgraph cluster by doing an [Initial import]({{< relref "bulk-loader.md" >}}) and you can import data into a running instance by performing a [Live import]({{< relref "live-loader.md" >}}).


Initial import is **considerably faster** than the live import but can only be used to load data into a new cluster (without prior data) and is executed before starting the Alpha nodes.

{{% notice "note" %}} Contact us if you need to do an initial import on a Dgraph Cloud instance.{{% /notice %}}


{{% notice "note" %}} Both options accept [RDF N-Quad/Triple
data](https://www.w3.org/TR/n-quads/) or JSON format. Refers to [data migration]({{< relref "about-data-migration.md" >}}) to see how to convert other data formats.{{% /notice %}}
