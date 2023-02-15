
+++
date = "2023-02-14T22:25:17+11:00"
title = "Provision a backend"
weight = 1
[menu.main]
    parent = "dgraphcloud"
+++

### Before you begin
Signup to [Dgraph Cloud](https://cloud.dgraph.io) using **Sign in with Google**, **Sign in with GitHub** or any other email account that you prefer to use.

### Provision a backend

1. After you have signed up and verified you email, log into
[Dgraph Cloud](https://cloud.dgraph.io/) and you'll arrive at the dashboard
screen.
{{< figure class="screenshot" src="/images/cloud/dgraph-cloud-empty-dashboard.png" title="first login empty dashboard" >}}


2. Click the **Launch New Backend** button and you'll be taken to a
screen to enter the details of the backend.


  Name the backend, optionally set a subdomain (if left blank, Dgraph Cloud picks
a random domain for you), and then pick a region to deploy you GraphQL backend to.

{{< figure class="screenshot" src="/images/cloud/dgraph-cloud-launch-backend.png" title="launch a backend" >}}


3. click **Launch** and your backend will be deployed in a few seconds.


{{< figure class="screenshot" src="/images/cloud/dgraph-cloud-backend-live.png" title="Dgraph Cloud console" >}}

That's it!  You now have a running Dgraph backend.  Time to build an app.

The URL listed in "GraphQL Endpoint" is the URL at which Dgraph Cloud will serve data to your app.

You can copy it at any time to use in a GraphQL client application.
