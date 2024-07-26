+++
title = "GraphQL Subscriptions"
description = "Subscriptions allow clients to listen to real-time messages from the server. In GraphQL, it’s straightforward to enable subscriptions on any type."
weight = 6
[menu.main]
  name = "Subscriptions"
  identifier = "subscriptions"
  parent = "graphql"

+++

Subscriptions allow clients to listen to real-time messages from the server. The client connects to the server with a bi-directional communication channel using the WebSocket protocol and sends a subscription query that specifies which event it is interested in. When an event is triggered, the server executes the stored GraphQL query, and the result is sent back to the client using the same communication channel.

The client can unsubscribe by sending a message to the server. The server can also unsubscribe at any time due to errors or timeouts. A significant difference between queries or mutations and subscriptions is that subscriptions are stateful and require maintaining the GraphQL document, variables, and context over the lifetime of the subscription.

![Subscription](/images/graphql/subscription_flow.png "Subscription in GraphQL")

## Enable subscriptions in GraphQL

In GraphQL, it's straightforward to enable subscriptions on any type. You can add the `@withSubscription` directive to the schema as part of the type definition, as in the following example:

```graphql
type Todo @withSubscription {
  id: ID!
  title: String!
  description: String!
  completed: Boolean!
}
```

## @withSubscription with @auth

You can use [@auth]({{< relref "graphql/schema/directives/auth">}}) access control rules in conjunction with `@withSubscription`.


Consider following Schema that has both the `@withSubscription` and `@auth` directives defined on type `Todo`. 

```graphql
type Todo @withSubscription @auth(
    	query: { rule: """
    		query ($USER: String!) {
    			queryTodo(filter: { owner: { eq: $USER } } ) {
    				__typename
    			}
   			}"""
     	}
   ){
        id: ID!
    	text: String! @search(by: [term])
     	owner: String! @search(by: [hash])
   }
# Dgraph.Authorization {"Header":"X-Dgraph-AuthToken","Namespace":"https://dgraph.io/jwt/claims","jwkurl":"https://xyz.clerk.accounts.dev/.well-known/jwks.json","audience":["dgraph"],"ClosedByDefault":true}
```
The generated GraphQL API expects a JWT token in the `X-Dgraph-AuthToken` header and uses the `USER` claim to apply a rule based access control (RBAC): the authorization rule enforces that only to-do tasks owned by `$USER` are returned.


## WebSocket client
Dgraph uses the websocket subprotocol `subscription-transport-ws`.

Clients must be instantiated using the WebSocket URL of the GraphQL API which is your [Dgraph GraphQL endpoint]({{< relref "graphql/graphql-clients/endpoint/_index.md">}}) with ``https`` replaced by ``wss``.

If your Dgraph endpoint is ``https://blue-surf-0033.us-east-1.aws.cloud.dgraph.io/graphql``
the WebSocket URL is ``wss://blue-surf-0033.us-east-1.aws.cloud.dgraph.io/graphql``

If your GraphQL API is configured to expect a JWT token in a header, you must configure the WebSocket client to pass the token. Additionally, the subscription terminates when the JWT expires.


Here are some examples of frontend clients setup.

### URQL client setup in a React application

In this scenario, we are using [urql client](https://formidable.com/open-source/urql/) and `subscriptions-transport-ws` modules.

In order to use a GraphQL subscription query in a component, you need to
- instantiate a subscriptionClient
- instantiate a URQL client with a 'subscriptionExchange' using the subscriptionClient

```js
import { Client, Provider, cacheExchange, fetchExchange, subscriptionExchange } from 'urql';
import { SubscriptionClient } from 'subscriptions-transport-ws';
  
  const subscriptionClient = new SubscriptionClient(
    process.env.REACT_APP_DGRAPH_WSS, 
    { reconnect: true,
      connectionParams: {"X-Dgraph-AuthToken" : props.token}
    }
    );
  
  const client = new Client({
    url: process.env.REACT_APP_DGRAPH_ENDPOINT,
    fetchOptions:  { headers: { "X-Dgraph-AuthToken":  `Bearer ${props.token}` } },
    exchanges: [
    cacheExchange,
    fetchExchange,
    subscriptionExchange({
      forwardSubscription: request => subscriptionClient.request(request),
    })
  ]})
  ```

In this example, 
  
- **process.env.REACT_APP_DGRAPH_ENDPOINT** is your [Dgraph GraphQL endpoint]({{< relref "graphql/graphql-clients/endpoint/_index.md">}}) 
- **process.env.REACT_APP_DGRAPH_WSS** is the WebSocket URL
- **props.token** is the JWT token of the logged-in user.

Note that we are passing the JWT token in the GraphQL client using 'fetchOptions' and in the WebSocket client using 'connectionParams'.

Assuming we are using graphql-codegen, we can define a subcription query:
```js
import { graphql } from "../gql";

export const TodoFragment = graphql(`
	fragment TodoItem on Todo {
		id
		text
	}
`)


export const  TodoSubscription = graphql(`
	subscription myTodo {
		queryTodo(first:100) {
			...TodoItem
		}
	}
`)
```
and use it in a React component 
```js
import { useQuery, useSubscription } from "urql";
...
const [messages] = useSubscription({ query: MyMessagesDocument});

```
That's it, the react component is able to use ``messages.data.queryTodo`` to display the updated list of Todos.


### Apollo client setup

To learn about using subscriptions with Apollo client, see a blog post on [GraphQL Subscriptions with Apollo client](https://dgraph.io/blog/post/how-does-graphql-subscription/).

To pass the user JWT token in the Apollo client,use `connectionParams`, as follows.

```javascript
const wsLink = new WebSocketLink({
  uri: `wss://${ENDPOINT}`,
  options: {
    reconnect: true,
    connectionParams: {  "<header>": "<token>", },});
```

Use the header expected by the Dgraph.Authorization configuration of your GraphQL schema.

## Subscriptions to custom DQL

You can also apply `@withSubscription` directive to custom DQL queries by specifying `@withSubscription` on individual DQL queries in `type Query`,
and those queries will be added to `type subscription`.

For example, see the custom DQL query `queryUserTweetCounts` below:

```graphql
type Query {
  queryUserTweetCounts: [UserTweetCount]  @withSubscription @custom(dql: """
	query {
		queryUserTweetCounts(func: type(User)) {
			screen_name: User.screen_name
			tweetCount: count(User.tweets)
		}
	}
	""")
}
```

`queryUserTweetCounts` is added to the `subscription` type, allowing users to subscribe to this query.

{{% notice "note" %}}
Currently, Dgraph only supports subscriptions on custom **DQL queries**. You
can't subscribe to custom **HTTP queries**.
{{% /notice %}}



{{% notice "note" %}}
Starting in release v21.03, Dgraph supports compression for subscriptions.
Dgraph uses `permessage-deflate` compression if the GraphQL client's
`Sec-Websocket-Extensions` request header includes `permessage-deflate`, as follows:
`Sec-WebSocket-Extensions: permessage-deflate`.
{{% /notice %}}

