+++
title = "Deploying on Dgraph Cloud"
description = "In just two steps on Dgraph Cloud (deployment & schema), you get a GraphQL API that you can easily use in any application."
weight = 7
type = "learn"
[menu.learn]
    parent = "todo-app-tutorial"
    identifier = "todo-app-deploy"
+++


In [Dgraph Cloud](https://cloud.dgraph.io/), an app is served by a GraphQL backend powered by Dgraph
database. You should deploy a backend for each app you build, and potentially
backends for test and development environments as well.

For this tutorial, you will just deploy one backend for development.

- Follow the instructions to [provision a backend]({{< relref "provision-backend.md">}})

{{< figure class="screenshot" src="/images/cloud/dgraph-cloud-backend-live.png" title="Dgraph Cloud console" >}}

The URL listed in "GraphQL Endpoint" is the URL at which Dgraph Cloud will serve data to your app.  You'll need that for later, so note it down --- though you'll always be able to access it from the dashboard.  There's nothing at that URL yet, first you need to design the GraphQL schema for the app.

Once the deployment is ready, let's add our schema there (insert your public key) by going to the schema tab.

```graphql
type Task @auth(
    query: { rule: """
        query($USER: String!) {
            queryTask {
                user(filter: { username: { eq: $USER } }) {
                    __typename
                }
            }
        }"""}), {
    id: ID!
    title: String! @search(by: [fulltext])
    completed: Boolean! @search
    user: User!
}
type User {
  username: String! @id @search(by: [hash])
  name: String
  tasks: [Task] @hasInverse(field: user)
}
# Dgraph.Authorization {"VerificationKey":"<AUTH0-APP-PUBLIC-KEY>","Header":"X-Auth-Token","Namespace":"https://dgraph.io/jwt/claims","Algo":"RS256","Audience":["<AUTH0-APP-CLIENT-ID>"]}
```

Once the schema is submitted successfully, we can use the GraphQL API endpoint.

Let's update our frontend to use this URL instead of localhost. Open `src/config.json` and update the `graphqlUrl` field with your GraphQL API endpoint.

```json
{
    ...
    "graphqlUrl": "<Dgraph-Cloud-GraphQL-API>"
}
```

That's it! Just in two steps on Dgraph Cloud (deployment & schema), we got a GraphQL API that we can now easily use in any application!
