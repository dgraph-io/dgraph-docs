+++
title = "Creating a Basic UI"
description = "Create a simple to-do app and integrate it with Auth0. This step in the GraphQL tutorial walks you through creating a basic UI with React."
weight = 3
type = "learn"
[menu.learn]
    parent = "todo-app-tutorial"
[nav]
  nextpage = "todo-auth-rules.md"
+++


In this step, we will create a simple to-do app (in React) and integrate it with Auth0.


## Create React app


Let's start by creating a React app using the `create-react-app` command.


```
npx create-react-app todo-react-app
```


To verify navigate to the folder, start the dev server, and visit [http://localhost:3000](http://localhost:3000).


```
cd todo-react-app
npm start
```


## Install dependencies


Now, let's install the various dependencies that we will need in the app.


```
npm install todomvc-app-css classnames graphql-tag history react-router-dom
```


## Setup Apollo Client


Let's start with installing the Apollo dependencies and then create a setup.


```
npm install @apollo/react-hooks apollo-cache-inmemory apollo-client apollo-link-http graphql apollo-link-context react-todomvc @auth0/auth0-react
```


Now, let's update our `src/App.js` with the below content to include the Apollo client setup.


```javascript
import React from "react"

import ApolloClient from "apollo-client"
import { InMemoryCache } from "apollo-cache-inmemory"
import { ApolloProvider } from "@apollo/react-hooks"
import { createHttpLink } from "apollo-link-http"

import "./App.css"

const createApolloClient = () => {
  const httpLink = createHttpLink({
    uri: "http://localhost:8080/graphql",
    options: {
      reconnect: true,
    },
  })


  return new ApolloClient({
    link: httpLink,
    cache: new InMemoryCache(),
  })
}


const App = () => {
  const client = createApolloClient()
  return (
    <ApolloProvider client={client}>
      <div>
        <h1>todos</h1>
        <input
          className="new-todo"
          placeholder="What needs to be done?"
          autoFocus={true}
        />
      </div>
    </ApolloProvider>
  )
}


export default App
```


Here we have created a simple instance of the Apollo client and passed the URL of our GraphQL API. Then we have passed the client to `ApolloProvider` and wrapped our `App` so that its accessible throughout the app.


## Queries and Mutations


Now, let's add some queries and mutations.


First, let's see how we can add a todo and get todos. Create a file `src/GraphQLData.js` and add the following.


```javascript
import gql from "graphql-tag"

export const GET_TODOS = gql`
  query {
    queryTodo: queryTask {
      id
      value: title
      completed
    }
  }
`

export const ADD_TODO = gql`
  mutation addTask($task: AddTaskInput!) {
    addTask(input: [$task]) {
      task {
        id
        value: title
        completed
      }
    }
  }
`
```


Now, let's see how to use this to add a todo.
Let's import the dependencies first in `src/App.js` replacing all the code.
Let's now create the functions to add a todo and get todos.


```javascript
import { useQuery, useMutation } from "@apollo/react-hooks"
import { Todos } from "react-todomvc"
import "react-todomvc/dist/todomvc.css"
import { useAuth0 } from "@auth0/auth0-react"
import { GET_TODOS, ADD_TODO } from "./GraphQLData"

function App() {
  const [add] = useMutation(ADD_TODO)

  const { user, isAuthenticated, loginWithRedirect, logout } = useAuth0();

  const { loading, error, data } = useQuery(GET_TODOS)
  if (loading) return <p>Loading</p>
  if (error) {
    return <p>`Error: ${error.message}`</p>
  }

  const addNewTodo = (title) =>
    add({
      variables: { task: { title: title, completed: false, user: { username: user.email } } },
      refetchQueries: [{
        query: GET_TODOS
      }]
    })

  return (
    <div>
      <Todos
        todos={data.queryTodo}
        addNewTodo={addNewTodo}
        todosTitle="Todos"
      />
    </div>
  )
}

export default App
```


## Auth0 Integration


Now, let's integrate Auth0 in our application and use that to add the logged-in user. Let's first create an app in Auth0.


- Head over to Auth0 and create an account. Click 'sign up' [here](https://auth0.com/)
- Once the signup is done, click "Create Application" in "Integrate Auth0 into your application".
- Give your app a name and select "Single Page Web App" application type
- Select React as the technology
- No need to do the sample app, scroll down to "Configure Auth0" and select "Application Settings".
- Select your app and add the values of `domain` and `clientid` in the file `src/auth_template.json`. Check this [link](https://auth0.com/docs/quickstart/spa/react/01-login#configure-auth0) for more information.
- Add `http://localhost:3000` to "Allowed Callback URLs", "Allowed Web Origins" and "Allowed Logout URLs".


Now that we have prepared our `src/App.js` file let's update our `src/index.js` file with the following code.

```javascript
import React from "react"
import ReactDOM from "react-dom"
import App from "./App"
import {
  ApolloClient,
  ApolloProvider,
  InMemoryCache,
  createHttpLink,
} from "@apollo/client"
import { setContext } from "@apollo/client/link/context"
import { Auth0Provider, useAuth0 } from "@auth0/auth0-react"
import config from "./auth_template.json"


const GRAPHQL_ENDPOINT = "http://localhost:8080/graphql"

const AuthorizedApolloProvider = ({ children }) => {
  const { isAuthenticated, getIdTokenClaims } = useAuth0();
  const httpLink = createHttpLink({
    uri: GRAPHQL_ENDPOINT,
  })

  const authLink = setContext(async (_, { headers }) => {
    if (!isAuthenticated) {
      return headers;
    }

    const token = await getIdTokenClaims();

    return {
      headers: {
        ...headers,
        "X-Auth-Token": token? token.__raw : "",
      },
    }
  })

  const apolloClient = new ApolloClient({
    link: authLink.concat(httpLink),
    cache: new InMemoryCache(),
  })

  return <ApolloProvider client={apolloClient}>{children}</ApolloProvider>
}

ReactDOM.render(
  <Auth0Provider
    domain={config.domain}
    clientId={config.clientId}
    redirectUri={window.location.origin}
  >
    <AuthorizedApolloProvider>
      <React.StrictMode>
        <App />
      </React.StrictMode>
    </AuthorizedApolloProvider>
  </Auth0Provider>,
  document.getElementById("root")
)
```

Note that for the application to work from this point on, the `src/auth_template.json` file must be configured with your auth0 credentials.

Here is a reference [Here](https://github.com/dgraph-io/auth-webinar/blob/marcelo/fix-finished-app/src/auth_template.json)



Let's also add definitions for updating, deleting and clearing all tasks to `src/GraphQLData.js`.
Let's also add the constants `user`, `isAuthenticated`, `loginWithRedirect` and `logout` which they receive from the variable `useAuth0`.
We also create a constant called `logInOut` that contains the logic to know if the user is logged in or not. This variable will show a button to login or logout depending on the status of logged in or logged out.
Note that before calling the component Todos we call our variable `{logInOut}` so that our login button appears above the application.


```javascript
import React from "react"
import { useQuery, useMutation } from "@apollo/client"
import { Todos } from "react-todomvc"

import "react-todomvc/dist/todomvc.css"
import { useAuth0 } from "@auth0/auth0-react"
import { GET_TODOS, ADD_TODO, UPDATE_TODO, DELETE_TODO, CLEAR_COMPLETED_TODOS  } from "./GraphQLData"

function App() {
  const [add] = useMutation(ADD_TODO)
  const [del] = useMutation(DELETE_TODO)
  const [upd] = useMutation(UPDATE_TODO)
  const [clear] = useMutation(CLEAR_COMPLETED_TODOS)

  const { user, isAuthenticated, loginWithRedirect, logout } = useAuth0();

  const { loading, error, data } = useQuery(GET_TODOS)
  if (loading) return <p>Loading</p>
  if (error) {
    return <p>`Error: ${error.message}`</p>
  }

  const addNewTodo = (title) =>
    add({
      variables: { task: { title: title, completed: false, user: { username: user.email } } },
      refetchQueries: [{
        query: GET_TODOS
      }]
    })

  const updateTodo = (modifiedTask) =>
    upd({
      variables: {
        id: modifiedTask.id,
        task: {
          value: modifiedTask.title,
          completed: modifiedTask.completed,
        },
      },
      update(cache, { data }) {
        data.updateTask.task.map((t) =>
          cache.modify({
            id: cache.identify(t),
            fields: {
              title: () => t.title,
              completed: () => t.completed,
            },
          })
        )
      },
    })

  const deleteTodo = (id) =>
    del({
      variables: { id },
      update(cache, { data }) {
        data.deleteTask.task.map(t => cache.evict({ id: cache.identify(t) }))
      },
    })

  const clearCompletedTodos = () =>
    clear({
      update(cache, { data }) {
        data.deleteTask.task.map(t => cache.evict({ id: cache.identify(t) }))
      },
    })

  const logInOut = !isAuthenticated ? (
    <p>
      <a href="#" onClick={loginWithRedirect}>Log in</a> to use the app.
    </p>
  ) : (
    <p>
      <a
        href="#"
        onClick={() => {
          logout({ returnTo: window.location.origin })
        }}
      >
        Log out
      </a>{" "}
      once you are finished, {user.email}.
    </p>
  );

  return (
    <div>
      {logInOut}
      <Todos
        todos={data.queryTodo}
        addNewTodo={addNewTodo}
        updateTodo={updateTodo}
        deleteTodo={deleteTodo}
        clearCompletedTodos={clearCompletedTodos}
        todosTitle="Todos"
      />
    </div>
  )
}

export default App
```

For our application to work correctly we need to update the `src/GraphQLData.js` file with the remaining queries.

```javascript
import gql from "graphql-tag"

export const GET_TODOS = gql`
  query {
    queryTodo: queryTask {
      id
      value: title
      completed
    }
  }
`

export const ADD_TODO = gql`
  mutation addTask($task: AddTaskInput!) {
    addTask(input: [$task]) {
      task {
        id
        value: title
        completed
      }
    }
  }
`

export const UPDATE_TODO = gql`
  mutation updateTask($id: ID!, $task: TaskPatch!) {
    updateTask(input: { filter: { id: [$id] }, set: $task }) {
      task {
        id
        value: title
        completed
      }
    }
  }
`

export const DELETE_TODO = gql`
  mutation deleteTask($id: ID!) {
    deleteTask(filter: { id: [$id] }) {
      task {
        id
      }
    }
  }
`

export const CLEAR_COMPLETED_TODOS = gql`
  mutation updateTask {
    deleteTask(filter: { completed: true }) {
      task {
        id
      }
    }
  }
`
```


Here is the complete code [Here](https://github.com/dgraph-io/auth-webinar/tree/marcelo/fix-finished-app/src)

Let's now start the app.


```
npm start
```


Now you should have an app running!



