
## Predicates declaration

The Dgraph Cluster **schema mode** defines if the Dgraph types must be declared before allowing mutations or not:
- In ``strict`` mode, you must declare the predicates before you can run a mutation using those predicates.
- In ``flexible`` mode (which is the default behavior), you can run a mutation without declaring the predicate in the DQL Schema.


:::note
When you deploy a [GraphQL API schema](/graphql), Dgraph generates all the underlying Dgraph types. 

Refer to [GraphQL and DQL schemas](/graphql/graphql-dql/graphql-dql-schema) in the [GraphQL - DQL interoperability](/graphql/graphql-dql) section for use cases using both approaches.
:::

For example, you can run the following mutation (using the [RDF](/dql/dql-rdf) notation):
```graphql
{
  set {
    <_:jedi1> <character_name> "Luke Skywalker" .
    <_:leia> <character_name> "Leia" .
    <_:sith1> <character_name> "Anakin" (aka="Darth Vador",villain=true).
    <_:sith1> <has_for_child> <_:jedi1> .
    <_:sith1> <has_for_child> <_:leia> .
  } 
}
```
In ``strict`` mode, the mutation will return an error if the predicates are not present in the Dgraph types schema.

In ``flexible`` mode, Dgraph will execute the mutation and adds the predicates “character_name” and “has_for_child” to the Dgraph types.


GrapHQL
- **`/admin/schema`** - Schema management
- **`/admin/schema/validate`** - Validate schema