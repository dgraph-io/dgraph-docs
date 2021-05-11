+++
title = "Lambda Fields"
description = "Start with lambda resolvers by defining it in your GraphQL schema. Then define your JavaScript mutation function and add it as a resolver in your JS source code."
weight = 2
[menu.main]
    parent = "lambda"
+++

### Schema

To set up a lambda function, first you need to define it on your GraphQL schema by using the `@lambda` directive.

For example, to define a lambda function for the `rank` and `bio` fields in `Author`: 

```graphql
type Author {
  id: ID!
  name: String! @search(by: [hash, trigram])
  dob: DateTime @search
  reputation: Float @search
  bio: String @lambda
  rank: Int @lambda
  isMe: Boolean @lambda
}
```

You can also define `@lambda` fields on interfaces, as follows:

```graphql
interface Character {
  id: ID!
  name: String! @search(by: [exact])
  bio: String @lambda
}

type Human implements Character {
  totalCredits: Float
}

type Droid implements Character {
  primaryFunction: String
}
```

### Resolvers

After the schema is ready, you can define your JavaScript mutation function and add it as a resolver in your JS source code. 
To add the resolver you can use either the `addGraphQLResolvers` or `addMultiParentGraphQLResolvers` methods.

{{% notice "note" %}}
A Lambda Field resolver can use a combination of `parents`, `parent`, `dql`, or `graphql` inside the function.
{{% /notice %}}

{{% notice "tip" %}}
This example uses `parent` for the resolver function. You can find additional resolver examples using `dql` in the [Lambda queries article]({{< relref "query.md" >}}), and using `graphql` in the [Lambda mutations article]({{< relref "mutation.md" >}}).
{{% /notice %}}

For example, to define JavaScript lambda functions for... 
- `Author`, 
- `Character`, 
- `Human`, and 
- `Droid`

...and add them as resolvers, do the following:

```javascript
const authorBio = ({parent: {name, dob}}) => `My name is ${name} and I was born on ${dob}.`
const characterBio = ({parent: {name}}) => `My name is ${name}.`
const humanBio = ({parent: {name, totalCredits}}) => `My name is ${name}. I have ${totalCredits} credits.`
const droidBio = ({parent: {name, primaryFunction}}) => `My name is ${name}. My primary function is ${primaryFunction}.`

self.addGraphQLResolvers({
  "Author.bio": authorBio,
  "Character.bio": characterBio,
  "Human.bio": humanBio,
  "Droid.bio": droidBio
})
```

For example, you can add a resolver for `rank` using a `graphql` call, as follows:

```javascript
async function rank({parents}) {
  const idRepList = parents.map(function (parent) {
    return {id: parent.id, rep: parent.reputation}
  });
  const idRepMap = {};
  idRepList.sort((a, b) => a.rep > b.rep ? -1 : 1)
    .forEach((a, i) => idRepMap[a.id] = i + 1)
  return parents.map(p => idRepMap[p.id])
}

self.addMultiParentGraphQLResolvers({
  "Author.rank": rank
})
```

The following example demonstrates using the client-provided JWT to return `true` if the custom claim
for `USER` from the JWT matches the `id` of the `Author`.

```javascript
async function isMe({ parent, authHeader }) {
  if (!authHeader) return false;
  if (!authHeader.value) return false;
  const headerValue = authHeader.value;
  if (headerValue === "") return false;
  const base64Url = headerValue.split(".")[1];
  const base = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  const allClaims = JSON.parse(atob(base64));
  if (!allClaims["https://my.app.io/jwt/claims"]) return false;
  const customClaims = allClaims["https://my.app.io/jwt/claims"];
  return customClaims.USER === parent.id;
}

self.addGraphQLResolvers({
  "Author.isMe": isMe,
});
```

### Example

For example, if you execute the following GraphQL query:

```graphql
query {
  queryAuthor {
    name
    bio
    rank
    isMe
  }
}
```

...you should see a response such as the following:

```json
{
  "queryAuthor": [
    {
      "name":"Ann Author",
      "bio":"My name is Ann Author and I was born on 2000-01-01T00:00:00Z.",
      "rank":3,
      "isMe": false
    }
  ]
}
```

In the same way, if you execute the following GraphQL query on the `Character` interface:

```graphql
query {
  queryCharacter {
    name
    bio
  }
}
```

...you should see a response such as the following:

```json
{
  "queryCharacter": [
    {
      "name":"Han",
      "bio":"My name is Han."
    },
    {
      "name":"R2-D2",
      "bio":"My name is R2-D2."
    }
  ]
}
```

{{% notice "Note" %}}
The `Human` and `Droid` types will inherit the `bio` lambda field from the `Character` interface. 
{{% /notice %}}

For example, if you execute a `queryHuman` query with a selection set containing `bio`, then the lambda function registered for `Human.bio` is executed, as follows:

```graphql
query {
  queryHuman {
    name
    bio
  }
}
```

This query generates the following response:

```json
{
  "queryHuman": [
    {
      "name": "Han",
      "bio": "My name is Han. I have 10 credits."
    }
  ]
}
```
