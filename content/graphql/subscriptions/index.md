+++
title = "GraphQL Subscriptions"
description = "Subscriptions allow clients to listen to real-time messages from the server. In GraphQL, it’s straightforward to enable subscriptions on any type."
weight = 8
[menu.main]
  name = "Subscriptions"
  identifier = "subscriptions"
  parent = "graphql"
+++

Subscriptions allow clients to listen to real-time messages from the server. The client connects to the server with a bi-directional communication channel using the WebSocket protocol and sends a subscription query that specifies which event it is interested in. When an event is triggered, the server executes the stored GraphQL query, and the result is sent back to the client using the same communication channel.

The client can unsubscribe by sending a message to the server. The server can also unsubscribe at any time due to errors or timeouts. A significant difference between queries or mutations and subscriptions is that subscriptions are stateful and require maintaining the GraphQL document, variables, and context over the lifetime of the subscription.

![Subscription](/images/graphql/subscription_flow.png "Subscription in GraphQL")

## How to enable subscriptions in GraphQL

In GraphQL, it's straightforward to enable subscriptions on any type. You can add the `@withSubscription` directive to the schema as part of the type definition, as in the following example:

```graphql
type Todo @withSubscription {
  id: ID!
  title: String!
  description: String!
  completed: Boolean!
}
```

### Example

After updating the schema with the `@withSubscription` directive, you can execute a subscription query and receive updates when the subscription query result is updated, as follows:

![Subscription](/images/graphql/subscription_example.gif "Subscription Example")

## Apollo client setup

To learn about using subscriptions with Apollo client, see a blog post on [GraphQL Subscriptions with Apollo client](https://dgraph.io/blog/post/how-does-graphql-subscription/).

## Subscriptions to custom DQL

You can use the `@withSubscription` directive on GraphQL types to generate subscription queries for that type.
You can also apply this directive to custom DQL queries by specifying `@withSubscription` on individual DQL queries in `type Query`,
and those queries will be added to `type subscription`.

{{% notice "note" %}}
Currently, Dgraph only supports subscriptions on custom DQL queries. So, you
can't subscribe to custom HTTP queries.
{{% /notice %}}

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

Because the `queryUserTweetCounts` query has a `@withSubscription` directive, it
will be added to the `subscription` type, allowing users to subscribe to this query.

## Authorization with subscriptions

Authorization adds more power to GraphQL subscriptions. You can use all of the authorization features that are available when running queries.
Additionally, you can specify when the subscription automatically terminates (the "timeout" of the subscription) in the JWT. 

### Schema
Consider following Schema that has both the `@withSubscription` and `@auth` directives defined on type `Todo`. The authorization rule enforces that only to-do tasks owned by `$USER` (defined in the JWT) are visible.

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
# Dgraph.Authorization {"VerificationKey":"secret","Header":"Authorization","Namespace":"https://dgraph.io","Algo":"HS256"}
```

### JWT

The subscription requires a JWT that declares the `$USER`, expiry, and other variables. 
The JWT is passed from the GraphQL client as key-value pair, where the key is the `Header` given in the schema and the value is the JWT.
In the example below, the key is `Authorization` and the value is the JWT. 

Most GraphQL clients have a separate header section to pass Header-JWT key-value pairs. In the Apollo client, these are passed
using `connectionParams`, as follows.

```javascript
const wsLink = new WebSocketLink({
  uri: `wss://${ENDPOINT}`,
  options: {
    reconnect: true,
    connectionParams: {  "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTAxMjg2MjIsImh0dHBzOi8vZGdyYXBoLmlvIjp7IlJPTEUiOiJVU0VSIiwiVVNFUiI6IkFsaWNlIn0sImlzcyI6InRlc3QifQ.6AODlumsk9kbnwZHwy08l40PeqEmBHqK4E_ozNjQpuI", },});
```

{{% notice "note" %}}
Starting in release v21.03, Dgraph supports compression for subscriptions.
Dgraph uses `permessage-deflate` compression if the GraphQL client's
`Sec-Websocket-Extensions` request header includes `permessage-deflate`, as follows:
`Sec-WebSocket-Extensions: permessage-deflate`.
{{% /notice %}}

### Example

The following example shows the operation of subscriptions with authentication rules for the schema given above.

First, you can generate the JWT as shown in the following image with expiry and `$USER` (the owner of a to-do task).
You can generate the JWT from [jwt.io](https://jwt.io/). The client should send the JWT to the server along with the request, as discussed above.

![Subscription-Generating-JWT](/images/graphql/Generating-JWT.png "Subscription with Auth Example")

Next, Dgraph runs the subscription and send updates. You can see that only the to-do tasks that were added with the owner name "Alice" are visible in the subscription.

![Subscription+Auth-Action](/images/graphql/Auth-Action.gif "Subscription with Auth Example")


Eventually, the JWT expires and the subscription terminates, as shown below.

![Subscription+Timeout](/images/graphql/Subscription-Timeout.gif "Subscription with Auth Example")

