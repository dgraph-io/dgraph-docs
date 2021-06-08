+++
date = "2017-03-20T19:35:35+11:00"
title = "Enterprise Features"
description = "Exclusive features like ACLs, binary backups, encryption at rest, and more are available with a Dgraph enterprise license, or with Dgraph Cloud dedicated instances."
weight = 9
[menu.main]
  identifier = "enterprise-features"
+++

<div class="landing">
  <div class="hero">
    <p>
      Exclusive features like ACLs, binary backups, encryption at rest, and more
      are available with a Dgraph enterprise license, or with Dgraph Cloud dedicated
      instances.
    </p>
    <img class="hero-deco" src="/images/hero-deco_403x160.png" />
  </div>
  <div class="item">
    <div class="icon"><i class="lni lni-download" aria-hidden="true"></i></div>
    <a  href="{{< relref "binary-backups.md">}}">
      <h2>Binary Backups</h2>
      <p>
        Full backups of Dgraph that are backed up directly to cloud storage
      </p>
    </a>
  </div>
  <div class="item">
    <div class="icon"><i class="lni lni-control-panel" aria-hidden="true"></i></div>
    <a href="{{< relref "access-control-lists.md">}}">
      <h2>Access Control Lists</h2>
      <p>
        ACL provides access protection to your data stored in Dgraph
      </p>
    </a>
  </div>
  <div class="item">
    <div class="icon"><i class="lni lni-lock-alt" aria-hidden="true"></i></div>
    <a href="{{< relref "encryption-at-rest.md">}}">
      <h2>Encryption at Rest</h2>
      <p>
        Ensure that sensitive data on disks is not readable by any user or application
      </p>
    </a>
  </div>
  <div class="item">
    <div class="icon"><i class="lni lni-keyword-research" aria-hidden="true"></i></div>
    <a  href="{{< relref "audit-logs.md">}}">
      <h2>Audit Logging</h2>
      <p>
        All requests are tracked and available for use in security audits. 
      </p>
    </a>
  </div>
    <div class="item">
    <div class="icon"><i class="lni lni-network" aria-hidden="true"></i></div>
    <a  href="{{< relref "multitenancy.md">}}">
      <h2>Multi-Tenancy</h2>
      <p>
        Multiple tenants co-exist in the same Dgraph cluster. 
      </p>
    </a>
  </div>
    <div class="item">
    <div class="icon"><i class="lni lni-files" aria-hidden="true"></i></div>
    <a  href="{{< relref "learner-nodes.md">}}">
      <h2>Learner Nodes</h2>
      <p>
        Spin-up a read-only replica instance across the world. 
      </p>
    </a>
  </div>
    <div class="item">
    <div class="icon"><i class="lni lni-cog" aria-hidden="true"></i></div>
    <a  href="{{< relref "change-data-capture.md">}}">
      <h2>Change Data Capture</h2>
      <p>
        Track data changes over time. 
      </p>
    </a>
  </div>  
  

</div>

<style>
  ul.contents {
    display: none;
  }
</style>
