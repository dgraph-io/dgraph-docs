+++
title = "Deploy the Schema"
type = "learn"
tutorial = "courses/messageboardapp/react"
pageType = "tutorial"
description = "Building a Message Board App in React. Step 2: With the schema defined, it’s just one step to get a running GraphQL backend for the app."
[menu.learn]
  name = "Deploy the Schema"
  parent = "react-app-graphql"
  identifier = "react-app-graphql-cloud"
  weight = 3
[nav.next]
title = "GraphQL Operations"
link = "/courses/messageboardapp/react/develop/graphql/graphql-operations/"
[nav.previous]
title = "The Schema as GraphQL"
link = "/courses/messageboardapp/react/develop/graphql/graphql-schema/"
+++

With the schema defined, it's just one step to get a running GraphQL backend for
the app.

Copy the schema, navigate to the **Schema** tab in Dgraph Cloud, paste the schema in, and press **Deploy**.

*![Deploy Dgraph Cloud Schema](/images/message-board/dgraph-cloud-deploy-schema-success.png)*

As soon as the schema is added, Dgraph Cloud generates and deploys a GraphQL API for the app.

Next you'll learn about GraphQL operations like queries, mutations and
subscriptions.
