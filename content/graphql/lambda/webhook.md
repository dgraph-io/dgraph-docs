+++
title = "Lambda Webhooks"
description = "Ready to use lambdas for webhooks? This documentation takes you through the schemas, resolvers, and examples."
weight = 5
[menu.main]
    parent = "lambda"
+++

### Schema

To set up a lambda webhook, you need to define it in your GraphQL schema by using the `@lambdaOnMutate` directive along with the mutation events (`add`/`update`/`delete`) you want to listen on.

{{% notice "note" %}}
Lambda webhooks only listen for events from the root mutation. You can create a schema that is capable of creating deeply nested objects, but only the parent level webhooks will be evoked for the mutation.
{{% /notice %}}

For example, to define a lambda webhook for all mutation events (`add`/`update`/`delete`) on any `Author` object:

```graphql
type Author @lambdaOnMutate(add: true, update: true, delete: true) {
    id: ID!
    name: String! @search(by: [hash, trigram])
    dob: DateTime
    reputation: Float
}
```

### Resolver

Once the schema is ready, you can define your JavaScript functions and add those as resolvers in your JS source code. 
To add the resolvers you should use the `addWebHookResolvers`method.

{{% notice "note" %}}
A Lambda Webhook resolver can use a combination of `event`, `dql`, `graphql` or `authHeader` inside the function.
{{% /notice %}}

#### Event object

You also have access to the `event` object within the resolver. Depending on the value of `operation` field, only one of the fields (`add`/`update`/`delete`) will be part of the `event` object. The definition of `event` is as follows:

```
"event": {
    "__typename": "<Typename>",
    "operation": "<one-of: add/update/delete>",
    "commitTs": <uint64, the commitTs of the mutation>
    "add": {
      "rootUIDs": [<list-of-UIDs-that-were-created-for-root-nodes-in-this-mutation>],
      "input": [<AddTypeInput: i.e. all the data that was received as part of the `input` argument>]
    },
    "update": {
      "rootUIDs": [<list-of-UIDs-of-root-nodes-for-which-somethig-was-set/removed-in-this-mutation>],
      "setPatch": <TypePatch: the object that was received as the patch for set>,
      "removePatch": <TypePatch: the object that was received as the patch for remove>
    },
    "delete": {
      "rootUIDs": [<list-of-UIDs-of-root-nodes-which-were-deleted-in-this-mutation>]
    }
```

#### Resolver examples

For example, to define JavaScript lambda functions for each mutation event for which `@lambdaOnMutate` is enabled and add those as resolvers:

```javascript
async function addAuthorWebhook({event, dql, graphql, authHeader}) {
    // execute what you want on addition of an author 
    // maybe send a welcome mail to the author
    
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

### Example

Finally, if you execute an `addAuthor` mutation, the `add` operation mapped to the `addAuthorWebhook` resolver will be triggered:

```graphql
mutation {
  addAuthor(input:[{name: "Ken Addams"}]) {
    author {
      id
      name
    }
  }
}
```
