+++
title = "React App Boiler Plate"
type = "learn"
tutorial = "courses/messageboardapp/react"
pageType = "tutorial"
description = "Jump right in thanks to the Message Board App Tutorial repo on GitHub. Get started with your Message Board App in React with GraphQL."
weight = 13
[menu.learn]
  name = "App Boiler Plate"
  parent = "react-app-ui"
  identifier = "react-app-ui-boilerplate"
[nav]
  nextpage = "connect-to-dgraph-cloud.md"
[nav.previous]
title = "Tech Stack"
link = "/courses/messageboardapp/react/develop/react/tech-stack/"
[nav.next]
title = "Connect to Dgraph Cloud"
link = "/courses/messageboardapp/react/develop/react/connect-to-dgraph-cloud/"
+++

## GitHub repo

All of the code for building the example React app shown in this tutorial is
available in GitHub in the [Message Board App Tutorial repo](https://github.com/dgraph-io/discuss-tutorial).

Each step in the tutorial is recorded as a tag on the `learn-tutorial` branch in
that repo. That means you can complete each step in the tutorial and also look
at the git diff if you're comparing what's described to the corresponding code
changes.

## Boilerplate

You'd start an app like this with `npx create-react-app ...` and then
`yarn add ...` to add the dependencies listed on the previous page (i.e., Tailwind CSS, Semantic
UI React, etc.)

This tutorial starts with the minimal boilerplate already complete. To read through the setup process that was used to build this tutorial, see this [blog about setting up a Dgraph Cloud app](https://dgraph.io/blog/post/slash-graphql-app-setup/).

For this tutorial, you can start with the boilerplate React app and CSS by
checking out the setup from GitHub. To do this, see the [tutorial-boilerplate tag](https://github.com/dgraph-io/discuss-tutorial/releases/tag/tutorial-boilerplate).

Note: in case you don't use git you can download minimal boilerplate as indicated in the previous link or you can do this using the `git` CLI as shown below.

```sh
git clone https://github.com/dgraph-io/discuss-tutorial
cd discuss-tutorial
git fetch --all --tags
git checkout tags/tutorial-boilerplate -b learn-tutorial
```

Alternatively, you can visit https://github.com/dgraph-io/discuss-tutorial/tags
and download the archive (**.zip** or **.tar.gz**) for the `tutorial-boilerplate`
tag.

## Running app boilerplate

After you have the boilerplate code on your machine, you can start the app
using the following `yarn` command:

```sh
yarn install
yarn start
```

This command builds the source and serves the app UI in development mode. The
app UI is usually served at `http://localhost:3000`, but the exact port may
vary depending on what else is running on your machine. Yarn will report the URL
as soon as it has the server up and running.

Navigate to the provided URL, and you'll see the boilerplate app running, as seen
below:

![running boiler plate app](/images/message-board/app-boilerplate.png)

At this point, you have just the CSS styling and minimal React setup. Next,
you'll move on to building the app.
