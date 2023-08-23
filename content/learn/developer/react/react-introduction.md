+++
title = "Introduction"
type = "learn"
description = "Introduction - Learn to deploy a GraphQL Backend, design a schema, and implement a React UI. This 2-hour course walks you through it."
aliases = ["/courses/messageboardapp/react/overview","/courses/messageboardapp/react","/courses/messageboardapp/"]
weight = 1
[menu.learn]
  name = "Introduction"
  identifier = "react-app-intro"
  parent = "react-app"
[nav]
nextpage =  "react-provision-backend.md"
+++


This tutorial walks you through building a reasonably complete message
board app. We selected this app because it's familiar and easy enough
to grasp the schema at a glance, but also extensible enough to add
things like integrated authorization and real-time updates with
subscriptions.

**Note:** This tutorial is a starting point and not the full version as shown in the images below, to check the final version of this app, access this [link](https://github.com/dgraph-io/discuss-tutorial/tree/master) clone the app and follow the steps described in the readme.

## The App

This app is designed to manage lists of posts in in different categories. A home
page lets each user view a feed of posts, as follows:


{{<figure class="medium image" src="/images/message-board/main-screenshot.png" title="message board app main page">}}


This app will use Dgraph Cloud's built-in authorization to allow public posts
that anyone can see (even without logging in) but restrict posting messages to
users who are logged-in. We'll also make some categories private, hiding them
from any users who haven't been granted viewer permissions. Users who are
logged-in can create new posts, and each post can have a stream of comments from
other users. A post is rendered on its own page, as follows:

{{<figure class="medium image" src="/images/message-board/post-screenshot.png" title="App post page">}}

This app will be completely serverless app:

*  Dgraph Cloud provides the "backend": a Dgraph database in a fully-managed
   environment
*  Auth0 provides serverless authentication
*  Netlify is used to deploy the app UI (the "frontend")


## Why use GraphQL?

You can build an app using any number of technologies, so why is GraphQL a good
choice for this app?

GraphQL is a good choice in many situations, but particularly where the app data
is inherently a *graph* (a network of data nodes) and where GraphQL queries let
us reduce the complexity of the UI code.

In this case, both are true. The data for the app is itself a graph; it's
about `users`, `posts` and `comments`, and the links between them. You'll naturally
want to explore that data graph as you work with the app, so GraphQL makes a
great choice. Also, in rendering the UI, GraphQL removes some complexity for
you.

If you built this app with REST APIs, for example, our clients (i.e., Web and
mobile) will have to programmatically manage getting all the data to render a
page. So, to render a post using a REST API, you will probably need to access
the `/post/{id}` endpoint to get the post itself, then the
`/comment?postid={id}` endpoint to get the comments, and then (iteratively for
each comment) access the `/author/{id}` endpoint. You would have to collect the
data from those endpoints, discard extra data, and then build a data structure
to render the UI. This approach requires different code in each version of the
app, and increases the engineering effort required and the opportunity for bugs
to occur in our app.  

With GraphQL, rendering a page is much simpler. You can run a single GraphQL
query that gets all of the data for a post (its comments and the authors of
those comments) and then simply lay out the page from the returned JSON. GraphQL
gives you a query language to explore the app's data graph, instead of having to
write code to build the data structure that you need from a series of REST API
calls.

## Why Dgraph Cloud?

Dgraph Cloud lets you build a GraphQL API for your app with just a GraphQL
schema, and it gets you to a running GraphQL API faster than any other tool.

Often, a hybrid model is used where a GraphQL API is layered over a REST API or
over a document or relational database. So, in those cases, the GraphQL layer
sits over other data sources and issues many queries to translate the REST or
relational data into something that looks like a graph. There's a cognitive jump
there, because your app is about a graph, but you need to design a relational
schema and work out how that translates into a graph. So, you'll think about the
app in terms of the graph data model, but always have to mentally translate back
and forth between the relational and graph models. This translation presents
engineering challenges, as well as an impact to query efficiency.

You don't have any of these engineering challenges with Dgraph Cloud.

Dgraph Cloud provides a fully-managed Dgraph database that stores all data
natively as a graph; it's a database of nodes and edges, with no relational
database running in the background. Compared to a hybrid model, Dgraph lets
you efficiently store, query and traverse data as a graph. Your data will get
stored just like you design it in the schema, and app queries are a single graph
query that fetches data in a format that can be readily consumed by your app.

With Dgraph Cloud, you design your application in GraphQL. You design a set of
GraphQL types that describes your requirements. Dgraph Cloud takes those types,
prepares graph storage for them, and generates a GraphQL API with queries and
mutations.

So, you can design a graph, store a graph and query a graph. You think and
design in terms of the graph that your app needs.

<!-- ## App architecture

You are going to build a serverless app here, ... Auth0, Netlify, Dgraph Cloud ... not the only choice for a Dgraph Cloud app, but a good one for lots of situations and for this tutorial.

**FIXME: design image in here about how the app will work**
**FIXME: maybe a couple of images, to pull things apart and make simpler, but has to show Dgraph Cloud backend, Auth provider, JWTs, frontend UI, in netlify.**
-->

## What's next

First, you will deploy a running Dgraph Cloud backend that will host our
GraphQL API. This gives you a working backend that you can use to build out your
app.

Then you will move on to the design process - it's graph-first, in fact, it's
GraphQL-first. After you design the GraphQL types that our app is based around,
Dgraph Cloud provides a GraphQL API for those types; then, you can move
straight to building your app around your GraphQL APIs.