+++
date = "2017-03-27:12:00:00Z"
title = "Dgraph Clients"
weight = 20
[menu.main]
    parent = "design-concepts"
+++

A client is a program that calls dgraph. Broadly, there are stand alone clients such as Ratel, which is a graphical web-based application, and programmatic client libraries which are embedded in larger programs to efficiently and idomatically call Dgraph.

GraphQL is an open standard with many clients (graphical and libraries) also, and GraphQL clients work with Dgraph.

Dgraph provides [client libraries]({{< relref "clients" >}}) for many languages. These clients send DQL queries, and perform useful functions such as logging in, in idomatic ways in each language.

Note that Dgraph does not force or insist on any particular GraphQL client. Any GraphQL client, GUI, tool, or library will work well with Dgraph, and it is the users' choice which to choose. Dgraph only provides clients for the proprietary DQL query language. GraphQL clients are available for free from many organizations.

However, Dgraph's cloud console does support basic GraphQL querying, so this is something of a tool. We recommend using a mature GraphQL console instead, as they are more mature. Dgraph's GraphQL GUI function is for quick start and convenience.
