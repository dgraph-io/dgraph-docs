+++
title = "Relationships"
description = "All the data in your app form a GraphQL data graph. That graph has nodes of particular types and relationships between the nodes to form the data graph."
weight = 2
type = "graphql"
[menu.graphql]
    parent = "gqlschema"
+++

All the data in your app form a GraphQL data graph. That graph has nodes of particular types and relationships between the nodes to form the data graph.

Dgraph uses the types and fields in the schema to work out how to link that graph, what to accept for mutations and what shape responses should take.  

Relationships in that graph are directed: either pointing in one direction or two.  You use the `@hasInverse` directive to tell Dgraph how to handle two-way relationship.

### One-way relationship

If you only ever need to traverse the graph between nodes in a particular direction, then your schema can simply contain the types and the relationship. 

In this schema, posts have an author - each post in the graph is linked to its author - but that relationship is one-way.  

```graphql
type Author {
    ...
}

type Post {
    ...
    author: Author
}
```

You'll be able to traverse the graph from a Post to its author, but not able to traverse from an author to all their posts.  Sometimes that's the right choice, but mostly, you'll want two way relationships.  

Note: Dgraph won't store the reverse direction, so if you change your schema to include a `@hasInverse`, you'll need to migrate the data to add the reverse edges.

### Two-way relationship


In Dgraph, the directive `@hasInverse` is used to create a two-way relationship.  

```graphql
type Author {
    ...
    posts: [Post] @hasInverse(field: author)
}

type Post {
    ...
    author: Author
}
```

With that, `posts` and `author` are just two directions of the same link in the graph.  For example,  adding a new post with

```graphql
mutation {
    addPost(input: [ 
        { ..., author: { username: "diggy" }}
    ]) {
        ...
    }
}
```

will automatically add it to Diggy's list of `posts`.  Deleting the post will remove it from Diggy's `posts`.  Similarly, using an update mutation on an author to insert a new post will automatically add Diggy as the author

```graphql
mutation {
    updateAuthor(input: {
        filter: { username: { eq: "diggy "}},
        set: { posts: [ {... new post ...}]}
    }) {
        ...
    }
}
```

### Many edges

It's not really possible to auto-detect what a schema designer meant for two-way edges.  There's not even only one possible relationship between two types. Consider, for example, if an app recorded the posts an `Author` had recently liked (so it can suggest interesting material) and just a tally of all likes on a post.

```graphql
type Author {
    ...
    posts: [Post]
    recentlyLiked: [Post]
}

type Post {
    ...
    author: Author
    numLikes: Int
}
```

It's not possible to detect what is meant here as a one-way edge, or which edges are linked as a two-way connection.  That's why `@hasInverse` is needed - so you can enforce the semantics your app needs.

```graphql
type Author {
    ...
    posts: [Post] @hasInverse(field: author)
    recentlyLiked: [Post]
}

type Post {
    ...
    author: Author
    numLikes: Int
}
```

Now, Dgraph will manage the connection between posts and authors and you can get on with concentrating on what your app needs to to - suggesting them interesting content.
