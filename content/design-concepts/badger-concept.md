+++
date = "2017-03-27:12:00:00Z"
title = "Badger (concept)"
weight = 20
[menu.main]
    parent = "design-concepts"
+++

##  Badger
[Badger](https://github.com/dgraph-io/badger) is a key-value store developed and maintained by Dgraph. It is also open source, and it is the backing store for Dgraph data. 

It is largely transparent to users that Dgraph uses Badger to store data internally. Badger is packaged into the Dgraph binary, and is the persistence layer. However, various configuration settings and log messages may reference Badger, such as cache sizes.

Badger values are `Posting Lists` and indexes. Badger Keys are formed by concatenating <RelationshipName>+<NodeUID>.
