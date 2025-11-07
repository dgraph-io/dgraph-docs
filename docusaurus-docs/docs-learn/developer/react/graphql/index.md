---
title: "Working in GraphQL"
description: "Developing a Message Board App in React with Dgraph Learn. Step 2: GraphQL schema design and loading, queries, and mutations."
---

To build an app with Dgraph Cloud, you design your application in GraphQL. You
design a set of GraphQL types that describes the app's data requirements. Dgraph Cloud
GraphQL takes those types, prepares graph storage for them and generates a
GraphQL API with queries and mutations.

In this section of the tutorial, you'll walk through the process of designing a
schema for a message board app, loading the GraphQL schema into Dgraph Cloud,
and then working through the queries and mutations that Dgraph Cloud makes available from that schema.

### In this section