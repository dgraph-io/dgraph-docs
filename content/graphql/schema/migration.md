+++
title = "Schema Migration"
description = "These documents describe all the things that you can put in your input GraphQL schema, and what gets generated from that."
weight = 1
[menu.main]
    parent = "schema"
    identifier = "schema-migration"
+++

There are many scenarios where Dgraph and GraphQL schema can differ which further can result in unexpected behaviour. 
This document will help users to identify these scenarios and prevent the unwanted behaviour, and also recover from these situations.

## Error messages

If you see an error message starting with below lines, it means you have changed schema in graphql which is not allowed in Dgraph, which results in different schemas in Dgraph and GraphQL.

```txt
resolving updateGQLSchema failed because succeeded in saving GraphQL schema but failed to alter Dgraph schema - GraphQL layer may exhibit unexpected behaviour, reapplying the old GraphQL schema may prevent any issues
```

It can be caused by various reasons , for example changing an list type to scalar , or changing an scalar field to uid.
Further if  you do query mutations on such schema you can get below errors depending upon the operation that you performed on schema update. 

 - `ErrExpectedScalar`   "An object type was returned, but GraphQL was expecting a scalar. This indicates an internal error -  probably a mismatch between the GraphQL and Dgraph/remote schemas. The value was resolved as null (which may trigger GraphQL error propagation)   and as much other data as possible returned. “    

 - `ErrExpectedSingleItem`  "A list was returned, but GraphQL was expecting just one item.  This indicates an internal error -  probably a mismatch between the GraphQL and Dgraph/remote schemas.  The value was resolved as null (which may trigger GraphQL error propagation)  and as much other data as possible returned."   

 - `ErrExpectedList`   "An item was returned, but GraphQL was expecting a list of items. This indicates an internal error - probably a mismatch between the GraphQL and Dgraph/remote schemas. The value was resolved as null (which may trigger GraphQL error propagation)  and as much other data as possible returned." 

There are some cases where you don’t get error at first place when you update the schema, but later you can get a error for invald operation.

For example, if you have field of type String! and add some data, later you change this to @id type then you may get problem while querying data , for example using get Query you will get multiple nodes with a given id , and get query will give error.

Basically it’s user responsibility to handle such cases , he shouldn’t do such invalid operations .

And if he needs such schema migration then he should be sure that it won’t cause any unexpected behaviour. For example, while changing normal field to @id filed  ,it’s user responsibility to make sure that his database  don’t have duplicate values for such fields.

## Examples

Changing list field to scalar

1.Post this schema
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

2. Add some data
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

3. change schema as below, i.e. change todo field to scalar
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

4.  it will give below error 

resolving updateGQLSchema failed because succeeded in saving GraphQL schema but failed to alter Dgraph schema - GraphQL layer may exhibit unexpected behaviour, reapplying the old GraphQL schema may prevent any issues: Schema change not allowed from [uid] => uid without deleting pred: owner.todo (Locations: [{Line: 3, Column: 4}])


5. Run below query 
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

it will return this error,
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
 
 So, the user needs to post his original schema to make this work.
 
 Example: Convert String! field to @id 

    Post this schema
```graphql
type todo {
  id : ID!
  task:String
}
```

2. Add this multiple times
```graphql
mutation {
  addtodo(input: { task: " bugs" }) {
    todo {
      task
    }
  }
}
```

3. change the schema to add @id field as below
```graphql
type todo {
  id : ID!
  task:String! @id
  }
```
  
  4. Run this mutation 
```graphql
mutation {
  addtodo(input: { task: " bugs" }) {
    todo {
      task
    }
  }
}
```

It will give below error 

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

and if we go get query bytask we will get below error 

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
