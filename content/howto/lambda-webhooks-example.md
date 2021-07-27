+++
date = "2017-09-10T22:25:17+11:00"
title = "Lambda Webhooks Example"
weight = 12
[menu.main]
    parent = "howto"
+++

It is a common need to populate a "Created At" date whenever a new data is created. Using Lambda [Webhooks]({{< relref "graphql/lambda/webhook.md#schema" >}}), the population of this field can be offloaded from the clients to a Dgraph Lambda. Lambda Webhooks are special kind of lambdas that are automatically invoked whenever data belonging to a GraphQL type is added, modified, or deleted.

Steps to run this example are as follows.

### The GraphQL Schema
```graphql
type Author @lambdaOnMutate(add: true, update: true, delete: true) {
    id: ID!
    name: String! @search(by: [hash, trigram])
    createdAt: DateTime
}
```

In the schema provided, there is a type `Author` which has an `id`, and `name` as well as a `createAt` field. The `createdAt` field is to be populated with the date when a new `Author` is created.

Please note that a special directive, `lambdaOnMutate` is configured. This configureation allowd Dgraph to invoke a lambda whenever an `Author` is added, updated or deleted.

### Configuring the lambda

```javascript
async function addAuthorWebhook({event, dql, graphql, authHeader}) {
    // execute what you want on addition of an author 
    // maybe send a welcome mail to the author
    console.log("new author added")
    console.log(event.add.rootUIDs[0])
    const createdDate = new Date()
    const createdAt = createdDate.toISOString();
    console.log(createdAt)
    const results = await graphql(`mutation UpdateCreatedDate($id: ID!, $createdAt: DateTime!) {
  updateAuthor(input: {filter: {id: [$id] }, set: {createdAt: $createdAt}}) {
    author {
      id
      name
      createdAt
    }
  }
}
`, {"id": event.add.rootUIDs[0], "createdAt" : createdAt})
    
}

async function updateAuthorWebhook({event, dql, graphql, authHeader}) {
    // execute what you want on updation of an author
    // maybe send a mail to the author informing that few details have been updated 
    
}

async function deleteAuthorWebhook({event, dql, graphql, authHeader}) {
    // execute what you want on deletion of an author
    // maybe mail the author saying they have been removed from the platform 
    
}

self.addWebHookResolvers({
    "Author.add": addAuthorWebhook,
    "Author.update": updateAuthorWebhook,
    "Author.delete": deleteAuthorWebhook,
})
```

The `addAuthorWebhook` function configured such that it is invoked whenever a new `Author` is added. The `addAuthorWebhook` receives an `event` object which contains the context of the add, update or delete action. In this example, the event contains the `uid` of the newly created `Author` in the field `event.add.rootUIDs[0]`.

### Mutation to add an Author

```graphql
mutation AddAuthor {
  addAuthor(input: {name: "John"}) {
    numUids
  }
}
```

This mutation will add an `Author`. Please note that only the `name` is provided by the client and the `createdAt` field is not provided by the client. Upon execution of this mutation, the `addAuthorWebhook` function configured previously will be invoked by Dgraph. This function retrieves the `uid` of the newly created `Author` and updates the `createdAt` attribute for this `uid`.

When you query the data subsequently, you will now see the following data. The `createdAt` field is now populated with a date.

```json
{
  "id": "0xd",
  "name": "John",
  "createdAt": "2021-07-16T05:28:06.433Z"
}
```

***Summary***

In this example, we saw an example of the lambda webhook using the `lambdaOnMutate` directive. We used a lambda webhook to auto-populate the `createdAt` attribute for a newly created `Author`. The advantage of this approach is that the client need not pass attributes that can be determined on the server side. This keeps the client code lightweight and easy to manage.
