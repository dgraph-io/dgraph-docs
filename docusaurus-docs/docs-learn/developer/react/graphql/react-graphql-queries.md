---
title: "GraphQL Queries"
description: "GraphQL queries are about starting points and traversals. From simple queries to deep filters, dive into the queries use in the message board app."
---


As we learned earlier, GraphQL queries are about starting points and traversals.
For example, a query can start by finding a post, and then traversing edges from
that post to find the author, category, comments and authors of all the comments.
![](/images/message-board/post2-search-in-graph.png)



## Dgraph Cloud Query

In the API that Dgraph Cloud built from the schema, queries are named for the
types that they let you query: `queryPost`, `queryUser`, etc. A query starts
with, for example, `queryPost` or by filtering to some subset of posts like
`queryPost(filter: ...)`. This defines a starting set of nodes in the graph.
From there, your query traverses into the graph and returns the subgraph it
finds. You can try this out with some example queries in the next section.

## Simple Queries

The simplest queries find some nodes and only return data about those nodes,
without traversing further into the graph. The query `queryUser` finds all users.
From those nodes, we can query the usernames as follows:

```graphql
query {
  queryUser {
    username
  }
}
```

The result will depend on how many users you have added.  If it's just the
`User1` sample, then you'll get a result like the following:

```json
{
  "data": {
    "queryUser": [
      {
        "username": "User1"
      }
    ]
  }
}
```

That says that the `data` returned is about the `queryUser` query that was executed
and here's an array of JSON about those users.

## Query by identifier

Because `username` is an identifier, there's also a query that finds users by ID.
To grab the data for a single user if you already know their ID, use the following
query:

```graphql
query {
  getUser(username: "User1") {
    username
  }
}
```

This time the query returns a single object, instead of an array.

```json
{
  "data": {
    "getUser": {
      "username": "User1"
    }
  }
}
```

## Query with traversal

Let's do a bit more traversal into the graph. In the example app's UI you can
display the homepage of a user. You might need to find a user's
data and some of their posts.

![](/images/message-board/user1-post-search-in-graph.png)


 Using GraphQL, you can get the same data using the following query:

```graphql
query {
  getUser(username: "User1") {
    username
    displayName
    posts {
      title
    }
  }
}
```

This query finds `User1` as the starting point, grabs the `username` and
`displayName`, and then traverses into the graph following the `posts` edges to
get the titles of all the user's posts.

A query could step further into the graph, finding the category of every post,
like this:

```graphql
query {
  getUser(username: "User1") {
    username
    displayName
    posts {
      title
      category {
        name
      }
    }
  }
}
```

Or, a query could traverse even deeper to get the comments on every post and the
authors of those comments, as follows:

```graphql
query {
  getUser(username: "User1") {
    username
    displayName
    posts {
      title
      category {
        name
      }
      comments {
        text
        author {
          username
        }
      }
    }
  }
}
```


## Querying with filters

To render the app's home screen, the app need to find a list of posts. Knowing
how to find starting points in the graph and traverse with a query means we can
use the following query to grab enough data to display a post list for the home
screen:

```graphql
query {
  queryPost {
    id
    title
    author {
      username
    }
    category {
      name
    }
  }
}
```

We'll also want to limit the number of posts displayed, and order them. For
example, we probably want to limit the number of posts displayed (at least until
the user scrolls) and maybe order them from newest to oldest.

This can be accomplished by passing arguments to `queryPost` that specify how we
want the result sorted and paginated.

```graphql
query {
  queryPost(
    order: { desc: datePublished }
    first: 10
  ) {
    id
    title
    author {
      username
    }
    category {
      name
    }
  }
}
```

The UI for your app also lets users search for posts. To support this, you added
`@search(by: [term])` to your schema so that Dgraph Cloud would build an API
for searching posts. The nodes found as the starting points in `queryPost` can
be filtered down to match only a subset of posts that have the term "graphql" in
the title by adding `filter: { title: { anyofterms: "graphql" }}` to the query,
as follows:

```graphql
query {
  queryPost(
    filter: { title: { anyofterms: "graphql" }}
    order: { desc: datePublished }
    first: 10
  ) {
    id
    title
    author {
      username
    }
    category {
      name
    }
  }
}
```

## Querying with deep filters

The same filtering works during a traversal. For example, we can combine the
queries we have seen so far to find `User1`, and then traverse to their posts,
but only return those posts that have "graphql" in the title.

```graphql
query {
  getUser(username: "User1") {
    username
    displayName
    posts(filter: { title: { anyofterms: "graphql" }}) {
      title
      category {
        name
      }
    }
  }
}
```

Dgraph Cloud builds filters and ordering into the GraphQL API depending on
the types and the placement of the `@search` directive in the schema. Those
filters are then available at any depth in a query, or in returning results from
mutations.

## Queries used in the message board app

The message board app used in this tutorial uses a variety of queries, some
of which are described and shown below:

The following query gets a user's information:

```graphql
query getUser($username: String!) {
  getUser(username: $username) {
    username
    displayName
    avatarImg
  }
}
```

The following query gets all categories. It is used to render the categories
selector on the main page, and to allow a user to select categories when adding
new posts:

```graphql
query {
  queryCategory {
    id
    name
  }
}
```

The followings gets an individual post's data when a user navigates to the
post's URL:

```graphql
query getPost($id: ID!) {
  getPost(id: $id) {
    id
    title
    text
    datePublished
    author {
      username
			displayName
      avatarImg
    }
    comments {
      text
      author {
        username
				displayName
      	avatarImg
      }
    }
  }
}
```

Next, you'll learn how to build your app's React UI.
