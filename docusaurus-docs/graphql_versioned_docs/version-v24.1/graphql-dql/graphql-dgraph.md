---
title: "GraphQL on Existing Dgraph"

---

### How to use GraphQL on an existing Dgraph instance

In the case where you have an existing Dgraph instance which has been created using a DQL Schema (and populated with Dgraph import tools) and you want to expose some or all of the data using a GraphQL API, you can use the [@dgraph directive](/graphql/schema/directives/directive-dgraph/) to customize how Dgraph maps GraphQL type names and fields names to DQL types and predicates.



### Language support in GraphQL

In your GraphQL schema, you need to define a field for each language that you want to use. 
In addition, you also need to apply the `@dgraph(pred: "...")` directive on that field, with the `pred` argument set to point to the correct DQL predicate with a language tag for the language that you want to use it for.
Dgraph will automatically add a `@lang` directive in the DQL schema for the corresponding predicate.

:::tip
By default, the DQL predicate for a GraphQL field is generated as `Typename.FieldName`.
:::

For example:

```graphql
type Person {
     name: String   # Person.name is the auto-generated DQL predicate for this GraphQL field, unless overridden using @dgraph(pred: "...")
     nameHi: String @dgraph(pred:"Person.name@hi") # this field exposes the value for the language tag `@hi` for the DQL predicate `Person.name` to GraphQL
     nameEn: String @dgraph(pred:"Person.name@en")
     nameHi_En:  String @dgraph(pred:"Person.name@hi:en") # this field uses multiple language tags: `@hi` and `@en`
     nameHi_En_untag:  String @dgraph(pred:"Person.name@hi:en:.") # as this uses `.`, it will give untagged values if there is no value for `@hi` or `@en`
  }
```

If a GraphQL field uses more than one language tag, then it won't be part of any mutation input. Like, in the above example the fields `nameHi_En` and `nameHi_En_untag` can't be given as an input to any mutation. Only the fields which use one or no language can be given in a mutation input, like `name`, `nameHi`, and `nameEn`.

All the fields can be queried, irrespective of whether they use one language or more.

:::note
GraphQL won’t be able to query `Person.name@*` type of language tags because of the structural requirements of GraphQL.
:::

### Bidirectional Relationships in Dgraph GraphQL

Dgraph provides two approaches for defining bidirectional relationships in GraphQL schemas. Each
approach has different tradeoffs regarding storage, DQL compatibility, and consistency management.

#### Overview

| Approach            | Directive               | DQL Predicates    | Storage | DQL `~` Support |
| ------------------- | ----------------------- | ----------------- | ------- | --------------- |
| **Dual Predicates** | `@hasInverse`           | 2 separate        | Doubled | ❌              |
| **Reverse Index**   | `@dgraph(pred: "~...")` | 1 with `@reverse` | Single  | ✅              |

---

#### Approach 1: `@hasInverse` (Dual Predicates)

##### GraphQL Schema

```graphql
type Post {
  id: ID!
  title: String!
  author: Author @hasInverse(field: "posts")
}

type Author {
  id: ID!
  name: String!
  posts: [Post]
}
```

##### Generated DQL Schema

```dql
Post.title: string .
Post.author: uid .
Author.name: string .
Author.posts: [uid] .

type Post {
    Post.title
    Post.author
}

type Author {
    Author.name
    Author.posts
}
```

##### How It Works

1. **Two separate predicates** are created: `Post.author` and `Author.posts`
2. The GraphQL **mutation layer maintains consistency** - when you set `Post.author`, it
   automatically updates `Author.posts`
3. Data is stored **twice** (once in each direction)

##### GraphQL Mutations

```graphql
mutation {
  addPost(input: [{ title: "My Post", author: { id: "0x123" } }]) {
    post {
      id
    }
  }
}
```

This generates DQL mutations for **both** directions:

```dql
{
    set {
        _:post <Post.title> "My Post" .
        _:post <Post.author> <0x123> .
        <0x123> <Author.posts> _:post .
    }
}
```

##### DQL Queries

```dql
# Forward: Post → Author
{
    posts(func: type(Post)) {
        Post.title
        Post.author {
            Author.name
        }
    }
}

# Reverse: Author → Posts (uses separate predicate)
{
    authors(func: type(Author)) {
        Author.name
        Author.posts {
            Post.title
        }
    }
}

# This does NOT work with @hasInverse:
{
    authors(func: type(Author)) {
        Author.name
        ~Post.author {   # No @reverse index exists!
            Post.title
        }
    }
}
```

##### When to Use

- You need the GraphQL layer to manage relationship consistency
- You're primarily using GraphQL and rarely use DQL directly
- You want simpler GraphQL schema syntax

---

#### Approach 2: `@dgraph(pred: "~...")` (Reverse Index)

##### GraphQL Schema

```graphql
type Post {
  id: ID!
  title: String!
  author: Author # Default predicate: Post.author
}

type Author {
  id: ID!
  name: String!
  posts: [Post] @dgraph(pred: "~Post.author")
}
```

> **Note:** The `@dgraph(pred: "Post.author")` directive on the forward edge is optional. Dgraph
> automatically names predicates as `TypeName.fieldName`, so `Post.author` is the default. You only
> need `@dgraph(pred: ...)` on the forward edge if you want a custom predicate name.

##### Generated DQL Schema

```dql
Post.title: string .
Post.author: uid @reverse .
Author.name: string .

type Post {
    Post.title
    Post.author
}

type Author {
    Author.name
}
```

##### How It Works

1. **One predicate** is created: `Post.author` with `@reverse` index
2. `Author.posts` is a **virtual field** - it maps to `~Post.author`
3. Data is stored **once**; reverse traversal uses the index
4. DQL automatically maintains consistency

##### GraphQL Mutations

```graphql
mutation {
  addPost(input: [{ title: "My Post", author: { id: "0x123" } }]) {
    post {
      id
    }
  }
}
```

This generates a DQL mutation for **only the forward edge**:

```dql
{
    set {
        _:post <Post.title> "My Post" .
        _:post <Post.author> <0x123> .
    }
}
```

The reverse is automatically available via `~Post.author`.

### DQL Queries

```dql
# Forward: Post → Author
{
    posts(func: type(Post)) {
        Post.title
        Post.author {
            Author.name
        }
    }
}

# Reverse: Author → Posts (uses @reverse index)
{
    authors(func: type(Author)) {
        Author.name
        ~Post.author {
            Post.title
        }
    }
}
```

##### When to Use

- You need DQL compatibility with `~predicate` syntax
- You want to minimize storage (data stored once, not twice)
- You're using both GraphQL and DQL APIs
- You prefer DQL's automatic consistency over GraphQL mutation rewriting

---

#### Important Constraints

##### Cannot Combine Both Approaches

You **cannot** use `@hasInverse` and `@dgraph(pred: "~...")` on the same relationship:

```graphql
# INVALID - Will produce a validation error
type Post {
  author: Author @hasInverse(field: "posts") @dgraph(pred: "~Author.posts")
}
```

Error:

```
@hasInverse directive is not allowed when pred argument in @dgraph directive starts with a ~
```

##### Predicate Naming

Dgraph automatically names predicates as `TypeName.fieldName`. The reverse field references this
default name:

```graphql
# Simple: Use default predicate naming
type Post {
  author: Author
}
type Author {
  posts: [Post] @dgraph(pred: "~Post.author")
}

# Also valid: Explicit predicate name (useful for custom naming)
type Post {
  author: Author @dgraph(pred: "wrote")
}
type Author {
  posts: [Post] @dgraph(pred: "~wrote")
}
```

---

#### Examples

##### Blog System

**Using `@hasInverse`:**

```graphql
type BlogPost {
  id: ID!
  title: String! @search(by: [term])
  content: String
  author: User @hasInverse(field: "posts")
  comments: [Comment] @hasInverse(field: "post")
}

type User {
  id: ID!
  username: String! @id
  posts: [BlogPost]
}

type Comment {
  id: ID!
  text: String!
  post: BlogPost
  author: User @hasInverse(field: "comments")
}
```

**Using `@dgraph(pred: "~...")`:**

```graphql
type BlogPost {
  id: ID!
  title: String! @search(by: [term])
  content: String
  author: User @dgraph(pred: "BlogPost.author")
  comments: [Comment] @dgraph(pred: "BlogPost.comments")
}

type User {
  id: ID!
  username: String! @id
  posts: [BlogPost] @dgraph(pred: "~BlogPost.author")
  comments: [Comment] @dgraph(pred: "~Comment.author")
}

type Comment {
  id: ID!
  text: String!
  post: BlogPost @dgraph(pred: "~BlogPost.comments")
  author: User @dgraph(pred: "Comment.author")
}
```

##### Movie Database

**Using `@dgraph(pred: "~...")` for DQL compatibility:**

```graphql
type Movie {
  id: ID!
  title: String! @search(by: [term, fulltext])
  releaseYear: Int @search
  director: Person @dgraph(pred: "Movie.director")
  actors: [Person] @dgraph(pred: "Movie.actors")
}

type Person {
  id: ID!
  name: String! @search(by: [hash, term])
  directed: [Movie] @dgraph(pred: "~Movie.director")
  actedIn: [Movie] @dgraph(pred: "~Movie.actors")
}
```

**DQL queries for this schema:**

```dql
# Find all movies directed by a person
{
    person(func: eq(Person.name, "Christopher Nolan")) {
        Person.name
        ~Movie.director {
            Movie.title
            Movie.releaseYear
        }
    }
}

# Find all actors in a movie
{
    movie(func: eq(Movie.title, "Inception")) {
        Movie.title
        Movie.actors {
            Person.name
        }
    }
}
```

---

#### Migration Guide

##### From `@hasInverse` to `@dgraph(pred: "~...")`

If you need to migrate an existing schema:

1. **Export your data** using the export API
2. **Update your GraphQL schema** to use `@dgraph(pred: "~...")`
3. **Transform exported data** to remove duplicate inverse edges
4. **Re-import data**

**Warning:** This is a breaking change. The DQL predicate structure changes, and existing DQL
queries may need updates.

##### Recommended Approach for New Projects

For new projects that will use both GraphQL and DQL:

- Use `@dgraph(pred: "~...")` for better DQL compatibility
- Explicitly name all predicates with `@dgraph(pred: "...")` for clarity

For GraphQL-only projects:

- Use `@hasInverse` for simpler syntax and automatic consistency management
