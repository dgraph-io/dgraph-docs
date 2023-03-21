+++
title = "Deploy a GraphQL Backend"
tutorial = "courses/messageboardapp/react"
type = "learn"
description = "Dgraph Learn - Build a Message Board App in React. Deploy a backend for each app you build with Dgraph Cloud."
[menu.learn]
  name = "Deploy a GraphQL Backend"
  identifier = "react-app-backend"
  parent = "react-app"
  weight = 2
[nav.next]
title = "Working in GraphQL"
link = "/learn/developer/react/graphql/"
[nav.previous]
title = "Introduction"
link = "/courses/messageboardapp/react/overview/introduction/"
+++

In Dgraph Cloud, an app is served by a GraphQL backend powered by Dgraph
database. You should deploy a backend for each app you build, and potentially
backends for test and development environments as well.

For this tutorial, you will just deploy one backend for development.

## Dgraph Cloud Dashboard

After you have signed up and verified you email, log into
[Dgraph Cloud](https://cloud.dgraph.io/) and you'll arrive at the dashboard
screen.

*![Dgraph Cloud: first login empty dashboard](/images/message-board/dgraph-cloud-empty-dashboard.png)*

Because you don't have any GraphQL backends yet, you won't have much on the
dashboard.  Click the **Launch New Backend** button and you'll be taken to a
screen to enter the details of the backend.

## Deploy a GraphQL backend

Name the backend, optionally set a subdomain (if left blank, Dgraph Cloud picks
a random domain for you), and then pick a region to deploy you GraphQL backend to.
For this tutorial, choose the free trial option.

*![Dgraph Cloud: launch a graphql backend](/images/message-board/dgraph-cloud-launch-backend.png)*

After you have the settings, click **Launch** and your backend will be deployed.
It takes a few seconds to deploy the infrastructure, but soon you'll have a
backend ready for the tutorial.

*![Dgraph Cloud: live backend](/images/message-board/dgraph-cloud-backend-live.png)*

That's it!  You now have a running GraphQL backend.  Time to build an app.

The URL listed in "GraphQL Endpoint" is the URL at which Dgraph Cloud will serve data to your app.  You'll need that for later, so note it down --- though you'll always be able to access it from the dashboard.  There's nothing at that URL yet, first you need to design the GraphQL schema for the app.

## Move on to schema design

Let's now move on to the design process - it's graph-first, in fact, it's
GraphQL-first. You'll design the GraphQL types that your app is based around,
learn about how graphs work and then look at some example queries and mutations.
