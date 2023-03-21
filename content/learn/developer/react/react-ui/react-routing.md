+++
title = "Routing in React"
type = "learn"
tutorial = "courses/messageboardapp/react"
pageType = "tutorial"
description = "Use React Router to build a message board app. A routing library in the UI interprets the URL path and renders an appropriate page for that path."
[menu.learn]
  name = "Routing in React"
  parent = "react-app-ui"
  identifier = "react-app-ui-routing"
  weight = 4
[nav.previous]
title = "Connect to Dgraph Cloud"
link = "/courses/messageboardapp/react/develop/react/connect-to-dgraph-cloud/"
[nav.next]
title = "GraphQL Queries"
link = "/courses/messageboardapp/react/develop/react/graphql-queries/"
+++

In a single-page application like this, a routing library in the UI interprets
the URL path and renders an appropriate page for that path.

## React Router

The routing library you'll be using in the app is
[React Router](https://reactrouter.com/web/guides/quick-start). It provides a
way to create routes and navigate between them. For example, the app's home URL
at `/` will render a list of posts, while `/post/0x123` will render the React
component for the post with id `0x123`.

Add dependencies to the project using the following commands:

```
yarn add react-router-dom
yarn add -D @types/react-router-dom
```

The `-D` option adds the TypeScript types `@types/react-router-dom` to the
project as a development dependency. Types are part of the development
environment of the project to help you build the app; but, in the build these
types are compiled away.

## Add components

You'll need components for the app to route to the various URLs. Create a
`src/components` directory, and then components for the home page
(`components/home.tsx`) and posts (`components/post.tsx`), with the following
file content:

```js
// components/home.tsx
import React from "react";

export function Home() {
  return <div>Home</div>;
}
```

```js
// components/post.tsx
import React from "react";

export function Post() {
  return <div>Post</div>;
}
```

You can leave those as boilerplate for now and fill them in when you add GraphQL
queries in the next step of this tutorial.

## Add routing

With the boilerplate components in place, you are now ready to add the routing
logic to your app. Edit `App.tsx` to add routes for the `home` and `post` views,
as shown below.

Note that the base URL points to the `home` component and `/post/:id` to the `post`
component. In the post component, `id` is used to get the data for the right post:

```js
...
import { Home } from "./components/home";
import { Post } from "./components/post";
import { BrowserRouter, Switch, Route } from "react-router-dom";

export function App() {
  return (
    <>
      <div className="app-banner">
        ...
      <div className="App">
        <div className="mt-4 mx-8">
          <p>
            Learn about building GraphQL apps with Dgraph Cloud at https://dgraph.io/learn
          </p>
          <BrowserRouter>
            <Switch>
              <Route exact path="/post/:id" component={Post} />
              <Route exact path="/" component={Home} />
            </Switch>
          </BrowserRouter>
        </div>
      </div>
    </>
  );
}
```

## This Step in GitHub

This step is also available in the
[tutorial GitHub repo](https://github.com/dgraph-io/discuss-tutorial)
with the [routing-in-react tag](https://github.com/dgraph-io/discuss-tutorial/releases/tag/routing-in-react)
and is [this code diff](https://github.com/dgraph-io/discuss-tutorial/commit/8d488e8c9bbccaa96c88fc49860021c493f1afca).

You can run the app using the `yarn start` command, and then you can navigate to
 `http://localhost:3000` and `http://localhost:3000/post/0x123` to see the
various pages rendered.
