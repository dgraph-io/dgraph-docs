+++
title = "Using Auth0"
type = "learn"
tutorial = "courses/messageboardapp/react"
pageType = "tutorial"
description = "Get an application running with Auth0. This step in the GraphQL tutorial walks you through using Auth0 in an example Message Board app tutorial."
weight = 18
[menu.learn]
  name = "Using Auth0"
  parent = "react-app-using-auth0"
  identifier = "react-app-using-auth0"
[nav]
	nextpage = "react-auth0.md"
[nav.previous]
title = "GraphQL Mutations"
link = "/docs/learn/developer/react/react-ui/"
[nav.next]
title = "Conclusion"
link = "/courses/messageboardapp/react/develop/conclusion/"
+++

Before we implement the login and logout system in our application make sure you have an auth0 account [auth0](https://auth0.com/).
With your auth0 account created, select create application and choose the single page application.
Now that you already have an account we can proceed with the tutorial.

<!-- Let's start by going to our Auth0 dashboard where we can see the application which we have already created and used in our frontend-application.

![Dashboard](/images/graphql/tutorial/todo/dashboard.png) -->

In your code editor terminal, run the command:
```sh
yarn add @auth/auth0-react
```

After installing the `auth0` library locate the file in the `src/components/header.tsx` folder and let's add some more code to make our authentication work.

First we must import the library into our `header.tsx` file.
```js
...
import { useAuth0, LogoutOptions } from '@auth0/auth0-react';
...
```
Next let's add the necessary constants along with the logic to show the `login` and `logout` buttons:
```js
...

const { isAuthenticated, loginWithRedirect, logout } = useAuth0();

const logInOut = !isAuthenticated ? (
	<span>
			<Button className="dgraph-btn mr-1">
			<a href="#" onClick={(event) => {
					event.preventDefault(); 
					loginWithRedirect()}}>Log in</a>
			</Button>
	</span>
	) : (
	<>
	<span>{addPostButton()}</span>
	<span>
			<Button className="dgraph-btn mr-1">
					<a
							href="#"
							onClick={() => {
									logout({ returnTo: window.location.origin } as LogoutOptions);
							} }
							>
					Log out
					</a>
			</Button>
	</span>
	</>
);
  ...
```
We're almost there, notice that we moved our `<span>{addPostButton()}</span>` into the login logic, because now we want the button to add a new post to only appear for the user when he is Logged. Now check if the code snippet inside the `header.tsx` file looks like this.
```js
...

return (
	<>
		{showCreatePost}
		<div className="ui clearing segment header-seg">
			<h3 className="ui right floated header header-seg-right">{logInOut}
			</h3>
			<h3 className="ui left floated header header-seg-left">
				<Link to="/">
					<div className="flex">
						<span>
							<Image size="tiny" src="/diggy.png" className="mr-5" />{" "}
						</span>
						<div>
							<p className="header-text">Dgraph</p>
							<p className="t-size">DISCUSS</p>
						</div>
					</div>
				</Link>
			</h3>
		</div>
	</>
  )
}
```
Done, now you can save the file, and run `yarn start` in the terminal.
