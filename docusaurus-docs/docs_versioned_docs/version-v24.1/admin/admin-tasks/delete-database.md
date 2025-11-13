---
title: Delete Database
---

To drop all data, you could send a `DropAll` request via `/alter` endpoint.

Alternatively, you could:

* [Shutdown Dgraph](shut-down-database) and wait for all writes to complete,
* Delete (maybe do an export first) the `p` and `w` directories, then
* Restart Dgraph.

:::warning
Always [export your data](export-database) before deleting the database to ensure you have a backup.
:::

## Related Topics

- [Export Database](export-database) - Create a backup before deletion
- [Shut Down Database](shut-down-database) - Clean shutdown before deletion
- [Secure Alter Operations](secure-alter-operations) - Protect against accidental drops

