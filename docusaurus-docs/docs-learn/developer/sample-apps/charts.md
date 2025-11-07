---
title: "Charts"
description: "A sample app for Dgraph database and Dgraph Cloud that lets you build online charts to visualize your metrics."
---

Charts is a sample app that lets users build online charts using metrics that
they provide. For example, you could provide this app with data from an
e-commerce site and use it to track site statistics such as the number of page
views and revenue. This app demonstrates how to use React hooks with Apollo
client to add and read related data. The repo for this app can be found on
GitHub at [dgraph.io/graphql-sample-apps/charting](https://github.com/dgraph-io/graphql-sample-apps/tree/master/charting).

### Features
- Create multiple metrics
- Data entry collection
- Plot metrics on line charts with controllable time period

### Front-end
- [React](https://reactjs.org/) (3.4.1)—a JavaScript library for building user interfaces.
- [Apollo Client](https://www.npmjs.com/package/apollo-client) (3.0+)—a comprehensive state management library for JavaScript that enables you to manage both local and remote data with GraphQL.
- [Material-UI](https://material-ui.com/)—a user interface framework for faster and easier web development.
- [React Google Charts](https://react-google-charts.com/)—a declarative API to make rendering charts fun and easy.

### Back-end
- [Dgraph Cloud](https://dgraph.io/cloud)—a fully managed GraphQL backend service
