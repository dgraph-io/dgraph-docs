+++
date = "2017-03-20T22:25:17+11:00"
title = "Running examples"
weight = 1   
[menu.main]
    parent = "query-language"
+++

This document provides the language reference for DQL.

The examples in this reference use a database of 21 million triples about movies and actors.

The queries are executed by an instance of Dgraph running at https://play.dgraph.io/.

#### Example database schema

The example movie database uses the following schema:

```
# Define Directives and index

director.film: [uid] @reverse .
actor.film: [uid] @count .
genre: [uid] @reverse .
initial_release_date: dateTime @index(year) .
name: string @index(exact, term) @lang .
starring: [uid] .
performance.film: [uid] .
performance.character_note: string .
performance.character: [uid] .
performance.actor: [uid] .
performance.special_performance_type: [uid] .
type: [uid] .

# Define Types

type Person {
    name
    director.film
    actor.film
}

type Movie {
    name
    initial_release_date
    genre
    starring
}

type Genre {
    name
}

type Performance {
    performance.film
    performance.character
    performance.actor
}
```
