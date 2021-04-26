+++
title = "Dgraph Releases"
[menu.main]
  name = "Releases"
  identifier = "releases"
  weight = 14
+++

The latest Dgraph release is the v21.03 series.

Dgraph releases starting with v20.03 follow
[calendar versioning](https://calver.org). To learn more about our switch from
semantic to calendar versioning, and why v2-v19 don't exist as a result of this
switch, see our Blog post on the 
[switch to calendar versioning](https://dgraph.io/blog/post/dgraph-calendar-versioning/).

To learn about the latest releases and other important announcements, watch the
[Announce][] category on Discuss.

[Announce]: https://discuss.dgraph.io/c/announce

## Dgraph release series

 Dgraph release series | Current release | Supported? | First release date | End of life
-----------------------|-----------------|------------|--------------------|--------------
 v21.03.x              | [v21.03.0][]    | Yes        | March 2021         | March 2022
 v20.11.x              | [v20.11.0][]    | Yes        | December 2020      | December 2021
 v20.07.x              | [v20.07.3][]    | Yes        | July 2020          | July 2021
 v20.03.x              | [v20.03.7][]    | No         | March 2020         | March 2021
 v1.2.x                | [v1.2.8][]      | No         | January 2020       | January 2021
 v1.1.x                | [v1.1.1][]      | No         | January 2020       | January 2021
 v1.0.x                | [v1.0.18][]     | No         | December 2017      | March 2020


[v21.03.0]: https://discuss.dgraph.io/t/release-notes-v21-03-0-resilient-rocket/13587
[v20.11.0]: https://discuss.dgraph.io/t/release-notes-v20-11-0-tenacious-tchalla/11942
[v20.07.3]: https://discuss.dgraph.io/t/dgraph-v20-07-3-release/12107
[v20.03.7]: https://discuss.dgraph.io/t/dgraph-v20-03-7-release/12077
[v1.2.8]: https://discuss.dgraph.io/t/dgraph-v1-2-8-release/11183
[v1.1.1]: https://discuss.dgraph.io/t/dgraph-v1-1-1-release/5664
[v1.0.18]: https://discuss.dgraph.io/t/dgraph-v1-0-18-release/5663

## Dgraph support policy

The following summarizes our approach to product and service support:
 
* **Dgraph releases**: Dgraph Labs supports Dgraph releases for 12 months following the
 first release date, until the applicable *End of life* date (see above).
* **Breaking API changes**: Occasionally, a new Dgraph release or Dgraph Cloud
service update will include breaking API changes. When this happens, Dgraph Labs
will provide advance notice to Dgraph customers so they can update their code 
to work with the breaking API change.
* **Data format changes**: Occasionally, Dgraph Cloud service updates will include
changes to the underlying data format. When this happens, Dgraph Labs will contact
Dgraph Cloud customers to schedule a short upgrade window. During the upgrade,
your Dgraph Cloud backend will switch to read-only.
* **Dgraph Cloud rolling upgrades**: Dgraph Cloud service updates that don't
include breaking API changes or data format changes are handled as rolling upgrades,
with no impact on HA clusters and minimal impact on non-HA clusters (non-HA
clusters switch to read-only during the upgrade).

<!-- Original API deprecation wording per Manish, for reviewer reference:  
If there're API breaking changes, we'll give the user plenty of notice (months) and work with them to upgrade them to the new version — this might require code changes at their end, so we have to be more careful.

If there're no API changes, but underlying data format changes, then we'd upgrade the user automatically based on the downtime slots the user chooses. Downtime for us means moving existing backend to "read-only" for 15-30 mins, and upgrading them.

If there're no underlying data changes, then we can just do a rolling upgrade, with no noticeable impact on HA clusters (but perhaps a couple of mins of downtime for non-HA clusters).
-->