---
title: Surveyo
description: A sample app for Dgraph database and Dgraph Cloud that lets create surveys.
pageType: sample-apps
image: /images/sample-apps/surveyo.svg
---

Surveyo is a sample app that provides users with a survey tool that they can use to quickly create and respond to surveys. Advanced users can use Surveyo’s GraphQL endpoint to run complex queries on survey results. This app demonstrates how to use React hooks with Apollo client to create surveys, collect responses, visualize responses with charts, export responses into CSV, and delete surveys. The repo for this app can be found on GitHub at [dgraph.io/graphql-sample-apps/surveyo](https://github.com/dgraph-io/graphql-sample-apps/tree/master/surveyo).

### Features
- Supports Short Answer, Multiple-Choice Question, Date Query and Rating type of questions
- Visualize responses collected as Pie Chart, Word Cloud and Bar chart
- Provides inline GraphiQL IDE to make GraphQL queries to chart data directly
- Export survey responses into CSV.

### Front-end
- [React](https://reactjs.org/) (3.4.1)—a JavaScript library for building user interfaces.
- [Apollo Client](https://www.npmjs.com/package/apollo-client) (3.1.1)—a comprehensive state management library for JavaScript that enables you to manage both local and remote data with GraphQL.
- [Auth0 React](https://github.com/auth0/auth0-react)—Auth0 SDK for React Single Page Applications (SPA).
- [AntDesign](https://ant.design/)—a design system for enterprise-level products.
- [Chart.js](https://www.chartjs.org/)—a simple yet flexible JavaScript charting for designers & developers
- [TypeScript](https://www.typescriptlang.org/)—extends JavaScript by adding types.
- [GraphiQL](https://github.com/graphql/graphiql)—a graphical interactive in-browser GraphQL IDE

### Back-end
- [Dgraph Cloud](https://dgraph.io/cloud)—a fully managed GraphQL backend service
- [Auth0](https://auth0.com/)—Secure access for everyone.
