+++
date = "2013-03-27T12:00:00Z"
title = "Lambdas"
type = "docs"
weight = 95
[menu.main]
    parent = "design-concepts"
+++

Dgraph Lambdas are JavaScript functions that can be used during query or mutation processing to extend GraphQL or DQL queries and mutations. Lambdas are not related at all to AWS Lambdas. They are functions that run in an (optional) node.js server that is included in the Dgraph Cloud offering. 
