+++
title = "Connect to Dgraph Cloud"
type = "learn"
tutorial = "courses/messageboardapp/react"
description = "Apollo client provides a connection to the GraphQL endpoint & a GraphQL cache that lets you manipulate the visual state of the app from the internal cache."
pageType = "tutorial"
[menu.learn]
  name = "Connect to Dgraph Cloud"
  parent = "react-app-ui"
  identifier = "react-app-ui-connect"
  weight = 3
[nav.previous]
title = "App Boilerplate"
link = "/courses/messageboardapp/react/develop/react/react-app-boiler-plate/"
[nav.next]
title = "React Routing"
link = "/courses/messageboardapp/react/develop/react/react-routing/"
+++

The GraphQL and React state management library you'll be using in the app is
[Apollo Client 3.x](https://www.apollographql.com/docs/react/).  

## Apollo client

For the purpose of this app, Apollo client provides a connection to a GraphQL endpoint and a GraphQL cache that lets you manipulate the visual state of the app from the internal cache. This helps to keep various components of the UI that rely on the same data consistent.

Add Apollo client to the project with the following command:

```
yarn add graphql @apollo/client
```

## Create an Apollo client

After Apollo client is added to the app's dependencies, create an
Apollo client instance that is connected to your Dgraph Cloud endpoint. Edit
`index.tsx` to add a function to create the Apollo client, as follows:

```js
const createApolloClient = () => {
  const httpLink = createHttpLink({
    uri: "<<Dgraph Cloud-GraphQL-URL>>",
  })

  return new ApolloClient({
    link: httpLink,
    cache: new InMemoryCache(),
  })
}
```

Make sure to replace `<<Dgraph Cloud-GraphQL-URL>>` with the URL of your Dgraph Cloud endpoint.  

If you didn't note the URL when you created the Dgraph Cloud backend, don't
worry, you can always access it from the Dgraph Cloud dashboard in the Overview tab.


## Add Apollo client to the React component hierarchy

With an Apollo client created, you then need to pass that client into the React
component hierarchy. Other components in the hierarchy can then use the
Apollo client's React hooks to make GraphQL queries and mutations.

Set up the component hierarchy with the `ApolloProvider` component as the root
component. It takes a `client` argument, which is the remainder of the app.
Change the root of the app in `index.tsx` to use the Apollo component as
follows.

```js
ReactDOM.render(
  <ApolloProvider client={createApolloClient()}>
    <React.StrictMode>
      <App />
    </React.StrictMode>
  </ApolloProvider>,
  document.getElementById("root")
)
```

## This step in GitHub

This step is also available in the [tutorial GitHub repo](https://github.com/dgraph-io/discuss-tutorial) with the [connect-to-slash-graphql tag](https://github.com/dgraph-io/discuss-tutorial/releases/tag/connect-to-slash-graphql) and is [this code diff](https://github.com/dgraph-io/discuss-tutorial/commit/56e86302d0d7e77d3861708b77124dab9aeeca61).

There won't be any visible changes from this step.
