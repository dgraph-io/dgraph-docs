
TO DO
--> what if a non mandatory parameter is not provided and used in the query !
--> what if a parameter is declared but never used in the query

TO-DO : which notation should be used to describe the grammar (BNF ?)
* `query title($name: string!, @age: int = "95") { ... }`

Example of query using Variables :

{{< runnable vars="{\"$a\": \"5\", \"$b\": \"10\", \"$name\": \"Steven Spielberg\"}" >}}
query test($a: int, $b: int, $name: string) {
  me(func: allofterms(name@en, $name)) {
    name@en
    director.film (first: $a, offset: $b) {
      name @en
      genre(first: $a) {
        name@en
      }
    }
  }
}
{{< /runnable >}}

Example of variables used in an arrays

{{< runnable vars="{\"$b\": \"10\", \"$aName\": \"Steven Spielberg\", \"$bName\": \"Quentin Tarantino\"}" >}}
query test($a: int = 2, $b: int!, $aName: string, $bName: string) {
  me(func: eq(name@en, [$aName, $bName])) {
    director.film (first: $a, offset: $b) {
      genre(first: $a) {
        name@en
      }
    }
  }
}
{{< /runnable >}}

## Submitting queries to Dgraph server
< TO DO : explain http and grpc enppoint and client - gives links to client page >
### Error Codes

When running a DQL query you might get an error message from the `/query` endpoint.
Here we will be focusing on the error `"code"` returned in the JSON error object.

You can usually get two types of error codes:
- [`ErrorInvalidRequest`](#errorinvalidrequest): this error can be either a bad request (`400`) or an internal server error (`500`).
- [`Error`](#error): this is an internal server error (`500`)

For example, if you submit a query with a syntax error, you'll get:

```json
{
  "errors": [
    {
      "message": "while lexing {\nq(func: has(\"test)){\nuid\n}\n} at line 2 column 12: Unexpected end of input.",
      "extensions": {
        "code": "ErrorInvalidRequest"
      }
    }
  ],
  "data": null
}
```
The error `"code"` value is returned with the query response.
In this case, it's a syntax error and the error `code` is `ErrorInvalidRequest`.

##### `Error`

This is a rare code to get and it's always an internal server error (`500`).
This can happen when JSON marsharling is failing (it's returned when the system tries to marshal a Go struct to JSON)

##### `ErrorInvalidRequest`

This is the most common error code that you can get from the `/query` endpoint. This error can be either a bad request (`400`) or an internal server error (`500`).

For example, you can get this error:
- If the query parameter is not being parsed correctly. The query parameter could be:
  - `debug`
  - `timeout`
  - `startTs`
  - `be` (best effort)
  - `ro` (read-only)
  - If the value of these query parameters is incorrect you would get this error code. This is basically a bad request (`400`)
- If the header's `Content-Type` value is not parsed correctly. The only allowed content types in the header are:
  - `application/json`
  - `application/dql`
  - `application/graphql+-` (deprecated)
  - Anything else will be wrongly parsed and end up in a bad request (`400`)
- Query timeout (deadline exceeded). This is an internal server error (`500`)
- Any error in query processing like:
  - syntax error - bad request (`400`)
  - health failing (server not healthy) - internal server error (`500`)
  - Alpha not able to reach zero because of network issue - internal server error (`500`)
  - ACL error (user not found or user does not have privileges) - unauthenticated/unauthorized request (`401` or `403`)
  - if you set `be=true` and `ro=false` - bad request (`400`)
  - any error related to JSON formatting the response - internal server error (`500`)


## Submitting queries to Dgraph
### Grpc
### HTTP Raw




For **HTTP requests** with parameters, we must use `Content-Type: application/json` header and pass data with a JSON object containing `query` and `variables`.

```sh
curl -H "Content-Type: application/json" localhost:8080/query -XPOST -d $'{
  "query": "query test($a: string) { test(func: eq(name, $a)) { \n uid \n name \n } }",
  "variables": { "$a": "Alice" }
}' | python -m json.tool | less
```

{{< runnable vars="{\"$a\": \"5\", \"$b\": \"10\", \"$name\": \"Steven Spielberg\"}" >}}
query test($a: int, $b: int, $name: string) {
  me(func: allofterms(name@en, $name)) {
    name@en
    director.film (first: $a, offset: $b) {
      name @en
      genre(first: $a) {
        name@en
      }
    }
  }
}
{{< /runnable >}}


* Any variable that is being used must be declared in the named query clause in the beginning.

{{< runnable vars="{\"$b\": \"10\", \"$name\": \"Steven Spielberg\"}" >}}
query test($a: int = 2, $b: int!, $name: string) {
  me(func: allofterms(name@en, $name)) {
    director.film (first: $a, offset: $b) {
      genre(first: $a) {
        name@en
      }
    }
  }
}
{{< /runnable >}}
### Clients
