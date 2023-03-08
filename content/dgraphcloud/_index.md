+++
title = "Dgraph Cloud"
[menu.main]
  identifier = "cloud"
  weight = 9
+++

<div class="landing">
  <div class="hero">
    <h1></h1>
    <p>
      Dgraph Cloud gives you the power of Dgraph database with the convenience of a fully-managed service.
    </p>
    <p>To learn more about Dgraph, see <a href="{{< relref "dgraph-overview.md">}}">Dgraph Database Overview</a>.</p>
    <img class="hero-deco" src="images/hero-deco.png" />
  </div>
  <div class="item">
    <div class="icon"><i class="lni lni-play" aria-hidden="true"></i></div>
    <a  href="{{< relref "cloud-quick-start.md">}}">
      <h2>Dgraph Cloud Quick Start</h2>
      <p>
        Get started with a simple "to-do" list app built on Dgraph Cloud
      </p>
    </a>
  </div>
  <div class="item">
    <div class="icon"><i class="lni lni-package" aria-hidden="true"></i></div>
    <a href="{{< relref "cloud-api/overview.md">}}">
      <h2>Dgraph Cloud API</h2>
      <p>
        Programmatically launch and manage your Cloud backups.
      </p>
    </a>
  </div>

  <div class="item">
    <div class="icon"><i class="lni lni-cogs" aria-hidden="true"></i></div>
    <a href="{{< relref "migrating-from-hosted-dgraph.md">}}">
      <h2>Migrate from Self-Managed Dgraph</h2>
      <p>
        Easily migrate your app's existing Dgraph backend to Dgraph Cloud
      </p>
    </a>
  </div>
  <div class="item">
    <div class="icon"><i class="lni lni-control-panel" aria-hidden="true"></i></div>
    <a href="{{< relref "admin/_index.md">}}">
      <h2>Administer Your Backend</h2>
      <p>
        Programmatically set and update your schema, import or export your data, and switch or clone your Dgraph Cloud backend
      </p>
    </a>
  </div>

</div>

<style>
  ul.contents {
    display: none;
  }
</style>

You might also be interested in:

- [Dgraph GraphQL Schema Reference](https://dgraph.io/docs/graphql/schema/schema-overview), which lists all the types and directives supported by Dgraph
- [Dgraph GraphQL API Reference](https://dgraph.io/docs/graphql/api/api-overview), which serves as a guide to using your new `/graphql` endpoint
