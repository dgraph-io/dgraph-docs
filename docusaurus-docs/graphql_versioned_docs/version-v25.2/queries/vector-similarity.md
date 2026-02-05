---
title: "Similarity Search"
description: "Dgraph automatically generates GraphQL queries for each vector index that you define in your schema. There are two types of queries generated for each index."

---

Dgraph automatically generates two GraphQL similarity queries for each type that have at least one [vector predicate](/graphql/schema/types/#vectors) with `@search` directive.

For example

```graphql
type User {
    id: ID!
    name: String!
    name_v: [Float!] @embedding @search(by: ["hnsw(metric: euclidean, exponent: 4)"])
}
```

With the above schema, the auto-generated `querySimilar<Object>ByEmbedding` query allows us to run similarity search using the vector index specified in our schema.

```graphql
getSimilar<Object>ByEmbedding(
    by: vector_predicate, 
    topK: n, 
    vector: searchVector): [User]
```

For example in order to find top 3 users with names similar to a given user name embedding the following query function can be used. 

```graphql  
querySimilarUserByEmbedding(by: name_v, topK: 3, vector: [0.1, 0.2, 0.3, 0.4, 0.5]) {
        id
        name
        vector_distance
     }
```
The results obtained for this query includes the 3 closest Users ordered by vector_distance. The vector_distance is the Euclidean distance between the name_v embedding vector and the input vector used in our query.

Note: you can omit vector_distance predicate in the query, the result will still be ordered by vector_distance.

The distance metric used is specified in the index creation. 

Similarly, the auto-generated `querySimilar<Object>ById` query allows us to search for similar objects to an existing object, given it’s Id. using the  function.

```graphql
getSimilar<Object>ById(
    by: vector_predicate, 
    topK: n, 
    id: userID):  [User]
```

For example the following query searches for top 3 users whose names are most similar to the name of the user with id "0xef7".

```graphql
querySimilarUserById(by: name_v, topK: 3, id: "0xef7") {
    id
    name
    vector_distance
}
```

