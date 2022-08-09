+++
date = "2017-03-20T22:25:17+11:00"
title = "External IDs and Upsert Block"
weight = 4
[menu.main]
    parent = "mutations"
+++

The upsert block provides a way to mutate the graph while using external IDs (xids).

Given the schema:
```DQL
xid: string @index(exact) .
name: string @index(exact) .
starring: [uid] @reverse .
birthdate: datetime .
year: int .

type Actor {
  xid
  name
  birthdate
}

type Movie {
  xid
  name
  starring
  year
}
```

Create initial data of a movie and an actor with external identifiers (example uses imdb identifiers).
```DQL
{
  set {
    _:nm0000705 <dgraph.type> "Actor" .
    _:nm0000705 <xid> "nm0000705" .
    _:nm0000705 <name> "Robin Wright" .

    _:tt0109830 <dgraph.type> "Movie" .
    _:tt0109830 <xid> "tt0109830" .
    _:tt0109830 <name> "Forest Gump" .
  }
}
```

Then you can link the two nodes by external identifiers and update nodes to add additional attributes.
```DQL
upsert {
  query {
    nm0000705 as var(func: eq(xid, "nm0000705"))
    tt0109830 as var(func: eq(xid, "tt0109830"))
  }
  mutation {
    set {
      uid(tt0109830) <starring> uid(nm0000705) .
      uid(nm0000705) <birthdate> "1966-04-08" .
      uid(tt0109830) <year> "1994" .
    }
  }
}
```



Query the data set by imdb external identifiers.
```DQL
{
  movie (func: eq(<xid>, "tt0109830")) {
    uid
    dgraph.type
    xid
    name
    year
    starring {
      uid
      dgraph.type
      xid
      name
      birthdate
    }
  }
}
```

You can also use an upsert block to update the xid itself.

The original data set mutation:
```DQL
{
  set {
    _:nm0000128 <dgraph.type> "Actor" .
    _:nm0000128 <xid> "nm0000128" .
    _:nm0000128 <name> "Tom Cruise" .
  }
}
```

Correct the xid using a delete and set in the same upsert mutation.
```DQL
upsert {
  query {
    nm0000128 as var(func: eq(xid, "nm0000128"))
  }
  mutation {
    delete {
      uid(nm0000128) <xid> "nm0000128" .
    }
    set {
      uid(nm0000128) <xid> "nm0000129" .
    }
  }
```

{{% notice "note" %}} This example uses the `S P O` delete method. For more information on delete methods see: https://dgraph.io/docs/mutations/delete/ {{% /notice %}}

It is possible that a singular node could have more than a singular external identifier. The important factor is that no two nodes share the same external identifer for the same predicate name. The predicate `xid` here is for an example, and could be of another name such as `uuid`. You could also use multiple predicates for unique external identifiers such as `imdb` and `rottentomatoes`.

## Advance Topic: Mixing DQL external identifiers with the GraphQL API

If using external identifiers with Dgraph’s GraphQL API, you can map the schema so all types reference the same external identifier predicate.
```GraphQL
# Dgraph's GraphQL Schema
type Movie {
  id: ID!
  xid: String! @id @dgraph(pred: "xid")
  name: String! @search(by: [exact])
  starring: [Actor] @hasInverse(field: "starringIn")
  year: Int
}

type Actor {
  id: ID!
  xid: String! @id @dgraph(pred: "xid")
  name: String! @search(by: [exact])
  starringIn: [Movie]
  birthdate: DateTime
}
```

Which would generate a DQL schema similar to:
```DQL
type Movie {
  xid
  Movie.name
  Movie.starring
  Movie.year
}
type Actor {
  xid
  Actor.name
  Actor.starringIn
  Actor.birthdate
}
xid: string @index(exact) .
Movie.name: string @index(exact) .
Movie.starring: [uid] .
Movie.year: int .
Actor.name: string @index(exact) .
Actor.starringIn: [uid] .
Actor.birthdate: datetime .
```

For more information on GraphQL <--> DQL schema mapping see: [New to Dgraph? DQL vs. GraphQL, Endpoints, Headers, and Schema Translation](https://discuss.dgraph.io/t/new-to-dgraph-dql-vs-graphql-endpoints-headers-and-schema-translation/10443)
