---
title: Connection
---

## Recent Servers

This section provides a list of recent connected clusters. You can select any item on the list to connect. 

The list also has an icon which indicates the version of the cluster running:

- Green icon: Running the latest version.
- Yellow icon: Running a specific version.
- Red icon: No connection found.
- Delete icon: Remove the address form the list.

![Ratel UI](/images/ratel/ratel_ui.png)


## URL Input box

In this box you add a valid Dgraph Alpha address. When you click on `Connect` Ratel will try to stablish a connection with the cluster. After Ratel has established a connection (all icons are green), click on the `Continue` button.

Under the input box you have tree icons which gives you the status of the connection.

- Network Access: Uses an "Energy Plug" icon.
- Server Health: Uses a "Heart" icon.
- Logging in: a "lock" icon.

:::tip
To connect to a standard Dgraph instance, you only need to click on `Connect`. There's a specific section to [login using ACL](#acl-account).
:::

## Cluster Settings

### ACL Account

The ACL Account login is necessary only when you have ACL features enabled.

:::note
The default password for a cluster started from scratch is `password` and the user is `groot`.
:::

### Dgraph Zero

If you use a custom address for Zero instance, you should inform here.

### Extra Settings

- Query timeout (seconds): This is a timeout for queries and mutations. If the operation takes too long, it will be dropped after `X` seconds in the cluster.
- Dgraph Cloud API Key: Used to access Dgraph Cloud services.

