---
title: "Data loading"

---



After you have deployed your first GraphQL Schema, you get a GraphQL API served on ``/graphql`` endpoint and an empty backend. You can populate the graph database using the mutations operations on the GraphQL API.

A more efficient way to populate the database is to use the Dgraph's [import tools](/graphql/[import-data](import-data)).

The first step is to understand the [schema mapping](/graphql/[graphql-dql-schema](graphql-dql-schema)) and to prepare your RDF files or JSON files to follow the internal Dgraph predicates names. 
You also have to make sure that you properly generate data for the `dgraph.type` predicate so that each node is asscociated with it's type.

If you are using the [initial import](/graphql/[bulk-loader](bulk-loader)) tool, you can provide the GraphQL schema along with the data to import when executing the bulk load.

If you are using the [live import](/graphql/[live-loader](live-loader)) tool, you must first deploy your GraphQL Schema and then proceed with the import. Deploying the schema first, will generate the predicates indexes and reduce the loading time.