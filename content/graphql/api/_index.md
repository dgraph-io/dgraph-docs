+++
title = "GraphQL Client"
weight = 80
[menu.main]
  identifier = "api"
  parent = "graphql"

+++

When you deploy a GraphQL schema, Dgraph serves the corresponding  [spec-compliant GraphQL](https://graphql.github.io/graphql-spec/June2018/) API at the HTTP endpoint `/graphql`


### gettint your GraphQL Endpoint

< to do> cloud and on prem tabs.

In Dgraph Cloud `/graphql` and `/admin` are served from the domain of your backend, which will be something like `https://YOUR-SUBDOMAIN.REGION.aws.cloud.dgraph.io`. If you are running a self-hosted Dgraph instance that will be at the alpha port and url (which defaults to `http://localhost:8080` if you aren't changing any settings).

### Tooling
