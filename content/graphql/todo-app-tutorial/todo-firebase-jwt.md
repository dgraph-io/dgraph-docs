+++
title = "Using Firebase Authentication"
weight = 6
[menu.main]
    parent = "todo-app-tutorial"
+++

In this step, we will add Firebase authentication per the sample [Todo app with Firebase Authentication](https://github.com/dgraph-io/graphql-sample-apps/tree/master/todo-react-firebase).

### Create Project

Let's start by going to the Firebase [website](https://firebase.google.com/) and create a new project (Todo-app).

![Firebase Create Project](/images/graphql/tutorial/todo/firebase-create-project.png)

![Firebase Dashboard](/images/graphql/tutorial/todo/firebase-dashboard.png)

In the **Authentication** section, enable `Email/Password` signin. You can add a custom domain to `Authorized domains` below according to where you want to deploy your app. By defaut localhost is added to the list. 

![Authentication Section](/images/graphql/tutorial/todo/firebase-domains.png)

Now we want to use the JWT that Firebase generates, but we also need to add custom claims to that token which will be used by our authorization rules.

To add custom claims to the JWT we need to host a cloud function which will insert claims into the JWT on user creation. This is our cloud function which inserts `USER`: `email` claim under the Namespace `https://dgraph.io/jwt/claims`.

```javascript
const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();

exports.addUserClaim = functions.https.onCall((data, context) => {
	return admin.auth().getUserByEmail(data.email).then(user=>{
		return admin.auth().setCustomUserClaims(user.uid, {
			"https://dgraph.io/jwt/claims":{
				"USER": data.email
			}
		});
	}).then(() => {
		return {
			message: `Success!`
		}
	}).catch(err => {
		 return err
	})
})
```

### Using the Firebase CLI

Clone the Todo Firebase app repo and try to deploy the function to the Firebase project created above.

```
git clone https://github.com/dgraph-io/graphql-sample-apps.git
cd graphql-sample-apps/todo-react-firebase
npm i
```

- Install the Firebase CLI tool `npm install -g firebase-tools`.
- Login into Firebase from the CLI `firebase login`.
- Run `firebase init functions` then select an existing project (that you created above).
- Select language as `JavaScript` for this example.
- Replace `index.js` with the snippet above.
- Deploy the function `firebase deploy --only functions.


Please refer to the [deployment guide](https://firebase.google.com/docs/functions/get-started) for more info.

![Firebase CLI](/images/graphql/tutorial/todo/firebase-cli.png)

### Create Webapp

Create a web app from your Firebase project settings page.

![Firebase Create Webapp](/images/graphql/tutorial/todo/firebase-create-webapp.png)

After creating that, copy the config from there.

![Firebase Config](/images/graphql/tutorial/todo/firebase-config.png)

Setup your Firebase configuration and `Dgraph Cloud` endpoint in the [config.json](https://github.com/dgraph-io/graphql-sample-apps/blob/master/todo-react-firebase/src/config.json). It looks like this:

```json
{
    "apiKey": "your-firebase-apiKey",
    "authDomain": "your-firebase-authDomain",
    "projectId": "your-firebase-projectId",
    "storageBucket": "your-firebase-storageBucket",
    "messagingSenderId": "your-firebase-messagingSenderId",
    "appId": "your-firebase-appId",
    "graphqlUrl": "your-graphql-endpoint"
}
```

Authentication with Firebase is done through the `JWKURL`, where the JSON Web Key sets are hosted by Firebase. Since Firebase shares the JWKs among multiple tenants, you must provide your Firebase `project-Id` to the `Audience` field. So the `Dgraph.Authorization` header will look like this:

```
{"Header":"your-header", "Namespace":"namespace-of-custom-claims","JWKURL": "https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com", "Audience":[your-projectID]}
```

You don't need to set the `VerificationKey` and `Algo` in the `Authorization` header. Doing so will cause an error.

Update the [schema](https://github.com/dgraph-io/graphql-sample-apps/blob/master/todo-react-firebase/schema.graphql), add the Authorization header (update the project-Id) -

```graphql
type Task @auth(
		query: { rule: """
        query($USER: String!) {
            queryTask {
                user(filter: { username: { eq: $USER } }) {
                    __typename
                }
            }
        }"""}
		add: { rule: """
        query($USER: String!) {
            queryTask {
                user(filter: { username: { eq: $USER } }) {
                    __typename
                }
            }
        }"""}){
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

# Dgraph.Authorization {"JWKUrl":"https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com", "Namespace": "https://dgraph.io/jwt/claims", "Audience": ["your-project-id"], "Header": "X-Auth-Token"}
```

Resubmit the updated schema to Dgraph or Dgraph Cloud.

### React App

For an example of how to initialize the Firebase app with the updated configuration (`config`) settings, see
[base.js](https://github.com/dgraph-io/graphql-sample-apps/blob/master/todo-react-firebase/src/base.js).

```javascript
import firebase from "firebase/app";
import "firebase/auth";
import config from "./config.json";


const app  = firebase.initializeApp({
  apiKey: config.apiKey,
  authDomain: config.authDomain,
  projectId: config.projectId,
  storageBucket: config.storageBucket,
  messagingSenderId: config.messagingSenderId,
  appId: config.appId
});

export default app;
```

To understand how the client gets the token and sends it along with each GraphQL request, see [Auth.js](https://github.com/dgraph-io/graphql-sample-apps/blob/master/todo-react-firebase/src/Auth.js). We can see from the code that whenever there will be `state` change, `currentUser` will be set to the `new user` and context will return `App` with the new `idToken`. `App` will initialize the Apollo Client which will send this `idToken` in header along with every GraphQL request.

```javascript
import React, { useEffect, useState } from "react";
import app from "./base.js";
import firebase from "firebase/app";
import "firebase/functions";

import App from "./App";
export const AuthContext = React.createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [idToken, setIdToken] = useState("");
  const addUserClaim = firebase.functions().httpsCallable('addUserClaim');

  useEffect(() => {
    app.auth().onAuthStateChanged( async user => {
      setLoading(false)
      setCurrentUser(user)
      if (user) {
        addUserClaim({email: user.email})
        const token = await user.getIdToken(); 
        setIdToken(token);
      }
    });
  }, []);

  if(loading){
    return <>Loading...</>
  }
  return (
    <AuthContext.Provider
      value={{
        loading,
        currentUser,
      }}
    >
      {children}
      <App idToken = {idToken}/>
    </AuthContext.Provider>
  );
};
```

To review the Apollo Client setup, see [App.js](https://github.com/dgraph-io/graphql-sample-apps/blob/master/todo-react-firebase/src/App.js).

```javascript
...

const createApolloClient = token => {
  const httpLink = createHttpLink({
    uri: config.graphqlUrl,
    options: {
      reconnect: true,
    },
  });

  const authLink = setContext((_, { headers }) => {
    // return the headers to the context so httpLink can read them
    return {
      headers: {
        ...headers,
        "X-Auth-Token": token,
      },
    };
  });

  return new ApolloClient({
    link: authLink.concat(httpLink),
    cache: new InMemoryCache()
  });
}

const App = ({idToken}) => {
  const { loading } = useContext(AuthContext);
  if (loading) {
    return <div>Loading...</div>;
  }
  console.log(idToken)
  const client = createApolloClient(idToken);
  return (
    <ApolloProvider client={client}>
      <div>
        <Router history={history}>
        <header className="navheader">
          <NavBar/>
        </header>
        <Switch>
        <PrivateRoute path="/" component= {TodoApp} exact />
        <PrivateRoute path="/profile" component={Profile} exact/>
        <Route exact path="/login" component = {Login} />
        <Route exact path="/signup" component={SignUp} />
      </Switch>
      </Router>
    </div>
    </ApolloProvider>
  );
}

export default App
```

Now that we have a basic understanding of how to integrate Firebase authentication in our app, let's see it in action!

```
npm start
```

![SignUp Screen](/images/graphql/tutorial/todo/firebase-webapp.png)

![Todos Screen](/images/graphql/tutorial/todo/firebase-todo.png)
