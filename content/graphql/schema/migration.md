+++
title = "Schema Migration"
description = "These documents describe all the things that you can put in your input GraphQL schema, and what gets generated from that."
weight = 1
[menu.main]
    parent = "schema"
    identifier = "schema-migration"
+++

There are many scenarios where Dgraph and GraphQL schemas can differ, which can result in unexpected behavior. 
This article will help you identify these scenarios and prevent unwanted behavior, and also recover from these situations.

## Error messages

If you see an error message starting with:

```txt
resolving updateGQLSchema failed because succeeded in saving GraphQL schema but failed to alter Dgraph schema - GraphQL layer may exhibit unexpected behaviour, reapplying the old GraphQL schema may prevent any issues
```

It means that you have changed a schema in GraphQL which is not allowed in Dgraph.
This will result in different schemas in Dgraph and GraphQL.
Such error can be caused by various reasons, for example changing a list type to scalar, or changing a scalar field to `uid`.

If you query mutations on such schemas, you can get the following errors, depending the operation that you performed on the schema update: 

 - `ErrExpectedScalar`: An object type was returned, but GraphQL was expecting a scalar. This indicates an internal error -  probably a mismatch between the GraphQL and Dgraph/remote schemas. The value was resolved as null (which may trigger GraphQL error propagation)   and as much other data as possible returned.

 - `ErrExpectedSingleItem`: A list was returned, but GraphQL was expecting just one item.  This indicates an internal error -  probably a mismatch between the GraphQL and Dgraph/remote schemas.  The value was resolved as null (which may trigger GraphQL error propagation)  and as much other data as possible returned.

 - `ErrExpectedList`: An item was returned, but GraphQL was expecting a list of items. This indicates an internal error - probably a mismatch between the GraphQL and Dgraph/remote schemas. The value was resolved as null (which may trigger GraphQL error propagation)  and as much other data as possible returned.
 
## Exceptions

There are some cases where you won't get an error when you update the schema, but you can get an error later for an invalid operation.

For example, if you have a `String!` field and add some data, when you change this field to the `@id` type you may have a problem while querying data. E.g., when using `getQuery` you will get multiple nodes with a given id, and get query will give an error.

If you need to perform such schema migrations, you should be sure that it won't cause any unexpected behavior.
For example, while changing a normal field to an `@id` field, it's the user's responsibility to make sure that the database doesn't have duplicate values for such fields.

## Examples

### List to scalar

Take for example changing a list field to scalar.

1.Post this schema:

```graphql
type todo {
  id: ID!    
  task: String   
  owner: owner
}  

type owner {
  name:String! @id 
  todo:[todo] @hasInverse(field:"owner")
}
```

2. Add some data:

```graphql
mutation {
  addtodo(
    input: [
      { task: "graphql bugs fix", owner: { name: "alice" } }
      { task: "dgraph bugs fix", owner: { name: "bob" } }
    ]
  ) {
    todo {
      taskowner {
        name
      }
    }
  }
}
```

3. Change the schema. E.g., change the `todo` field to scalar:

```graphql
type todo {
  id : ID!
  task:String
  owner:owner
}

type owner {
   name:String! @id
   todo:todo @hasInverse(field:"owner")
 }
```

4. The change will bring the following error: 

```txt
resolving updateGQLSchema failed because succeeded in saving GraphQL schema but failed to alter Dgraph schema - GraphQL layer may exhibit unexpected behaviour, reapplying the old GraphQL schema may prevent any issues: Schema change not allowed from [uid] => uid without deleting pred: owner.todo (Locations: [{Line: 3, Column: 4}])
```

5. Next, run the following query:

```graphql
query {
  queryowner {
    name
    todo {
      id
      task
    }
  }
}
```

it will return this error:

```json
"errors": [
    {
      "message": "A list was returned, but GraphQL was expecting just one item. This indicates an internal error - probably a mismatch between the GraphQL and Dgraph/remote schemas. The value was resolved as null (which may trigger GraphQL error propagation) and as much other data as possible returned.",
      "locations": [
        {
          "line": 5,
          "column": 4
        }
      ],
      "path": [
        "queryowner",
        0,
        "todo"
      ]
    },
 ```
 
You need to post the original schema to make this query work.

### `String!` to `@id`

Take for example changing a `String!` field to `@id`.

1. Post this schema:

```graphql
type todo {
  id : ID!
  task:String
}
```

2. Add this entry multiple times:

```graphql
mutation {
  addtodo(input: { task: " bugs" }) {
    todo {
      task
    }
  }
}
```

3. Change the schema to add the `@id` field:

```graphql
type todo {
  id : ID!
  task:String! @id
  }
```
  
4. Run the mutation:

```graphql
mutation {
  addtodo(input: { task: " bugs" }) {
    todo {
      task
    }
  }
}
```

It will give the following error:

```json
{
  "errors": [
    {
      "message": "mutation addtodo failed because Found multiple nodes with ID: 0x9c44",
      "locations": [
        {
          "line": 2,
          "column": 3
        }
      ]
    }
  ]
}
```

If you try to execute the `bytask` query you will get this error:

```json
{
  "errors": [
    {
      "message": "A list was returned, but GraphQL was expecting just one item. This indicates an internal error - probably a mismatch between the GraphQL and Dgraph/remote schemas. The value was resolved as null (which may trigger GraphQL error propagation) and as much other data as possible returned.",
      "locations": [
        {
          "line": 2,
          "column": 1
        }
      ],
      "path": [
        "gettodo"
      ]
    }
  ]
}
```
