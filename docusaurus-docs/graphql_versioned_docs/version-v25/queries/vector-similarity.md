---
title: "Similarity Search"
description: "Dgraph automatically generates GraphQL queries for each vector index that you define in your schema. There are two types of queries generated for each index."

---

Dgraph automatically generates two GraphQL similarity queries for each type that have at least one [vector predicate](/graphql/schema/types/#vectors) with the `@search` directive.

For example

```graphql
type User {
    id: ID!
    email: String! @id
    name: String!
    bio: String!
    bio_v: [Float!] @embedding @search(by: ["hnsw(metric: euclidean, exponent: 4)"])
}
```

With the above schema, the auto-generated `querySimilar<Object>ByEmbedding` query allows us to run similarity search using the vector index specified in our schema.

```graphql
querySimilar<Object>ByEmbedding(
    by: vector_predicate, 
    topK: n, 
    vector: searchVector,
    ef: Int,
    distance_threshold: Float): [User]
```

Query parameters:

* by: required, the vector predicate to which `vector` is compared
* topK: required, the number of matches to return
* vector: required, the search vector
* ef: optional, (effort) controls how many candidates the HNSW algorithm explores during search. Higher values improve recall (finding true nearest neighbors) at the cost of increased latency. Use this to tune the speed/accuracy tradeoff for individual queries when the index-level `efSearch` default doesn't fit your needs
* distance_threshold: optional, filters results to only return vectors within the specified distance (for euclidean) or above the specified similarity score (for cosine/dot product). Use this when you need results that meet a minimum quality threshold rather than just the `topK` nearest. Note: Since filtering is applied after the top-k search, specifying a small `topK` may limit the pool of candidates before filtering, potentially returning fewer results than expected. Consider increasing `topK` when using `distance_threshold` to ensure enough candidates are evaluated.
 
For example, in order to find top three Users with bios similar to a generated bio embedding, the following query function can be used

```graphql
querySimilarUserByEmbedding(by: bio_v, topK: 3, vector: [0.1, 0.2, 0.3, 0.4, 0.5]) {
        id
        name
        vector_distance
     }
```

The results obtained for this query includes the three closest Users by bio (including the source), ordered by the reserved, calculated field named `vector_distance`. No other ordering is available. Note that you can omit `vector_distance` predicate in the query, however the results will still be ordered by it.

:::note
For cosine and dot product metrics, vector_distance is computed as 1 - similarity, converting the similarity score into a distance where 0 indicates identical vectors and larger values indicate less similarity. This allows all similarity search results (regardless of metric) to be sorted in ascending order by distance, with the most similar results appearing first.
:::

Similarly, the auto-generated `querySimilar<Object>ById` query allows us to search for similar objects to an existing object, given its Id.

```graphql
querySimilar<Object>ById(
    by: vector_predicate, 
    topK: n, 
    id: userID,
    ef: Int,
    distance_threshold: Float):  [User]
```

Query Parameters:

* by: required, the vector predicate to which other nodes are compared
* topK: required, the number of matches to return
* id: potentially optional (see below), the node id from which the search begins
* ef: optional, (effort) controls how many candidates the HNSW algorithm explores during search. Higher values improve recall (finding true nearest neighbors) at the cost of increased latency. Use this to tune the speed/accuracy tradeoff for individual queries when the index-level `efSearch` default doesn't fit your needs
* distance_threshold: optional, filters results to only return vectors within the specified distance (for euclidean) or above the specified similarity score (for cosine/dot product). Use this when you need results that meet a minimum quality threshold rather than just the `topK` nearest. Note: Since filtering is applied after the top-k search, specifying a small `topK` may limit the pool of candidates before filtering, potentially returning fewer results than expected. Consider increasing `topK` when using `distance_threshold` to ensure enough candidates are evaluated.

If one of your type's fields has the `@id` directive, that field will also be included as an query input parameter. In which case, you can use that instead of the `id` parameter. Considering the example schema above, because the `email` field has the `@id` directive, the input object for this query would also contain `email: String`.

The following query searches for top three Users whose bio vectors are most similar to the that of the user with id "0xef7". Note that the User representing "0xef7" will be the first item in the results.

```graphql
querySimilarUserById(by: bio_v, topK: 3, id: "0xef7") {
    id
    name
    vector_distance
}
```

This query shows using the `email` input field instead:

```graphql
querySimilarUserById(by: bio_v, topK: 5, email: "bob@example.com") {
    id
    name
    vector_distance
}
```

:::note
Dgraph does not automatically generate embeddings. In the above examples, inserts into the graph included embeddings that were generated prior to mutation.
:::
