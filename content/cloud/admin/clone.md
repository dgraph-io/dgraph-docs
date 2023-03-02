+++
title = "Cloning Backend"
weight = 7
[menu.main]
    parent = "cloud-admin"
+++

Cloning a backend allows making a copy of an existing backend. The clone will be created with all the data and schema of the original backend present at the time of cloning. The clone will have its own endpoint and will be independent of the original backend once it is created. Any further changes in either backends will not reflect in the other. Currently, a clone can only be created in the same zone as that of the original backend.

In order to clone your backend, click on the <kbd>Clone Backend</kbd> button under the [Settings](https://cloud.dgraph.io/_/settings) tab in the dashboard's sidebar.

You can also perform the restore operation on an existing backend if you have an unused backend or want to reuse an existing endpoint. But note that the restore operation will drop all the existing data along with schema on the current backend and replace it with the original backend's data and schema.
