---
title: License
description: Apply and manage Dgraph Enterprise licenses
---

Dgraph enterprise features are proprietary licensed under the [Dgraph Community License][dcl]. All Dgraph releases contain proprietary code for enterprise features. Enabling these features requires an enterprise contract from [contact@dgraph.io](mailto:contact@dgraph.io) or the [discuss forum](https://discuss.dgraph.io).

**Dgraph enterprise features are enabled by default for 30 days in a new cluster.** After the 30-day trial period, the cluster must obtain a license from Dgraph to continue using enterprise features.

:::note
At the conclusion of your 30-day trial period, if a license has not been applied to the cluster, access to enterprise features will be suspended. The cluster will continue to operate without enterprise features.
:::

## Apply License

Apply an enterprise license key to the cluster using one of the following methods:

**HTTP endpoint** (POST request to any Zero server):

```sh
curl -X POST localhost:6080/enterpriseLicense --upload-file ./licensekey.txt
```

**Command-line flag** (useful for automation):

```sh
dgraph zero --enterprise_license ./licensekey.txt
```

## License Expiry Warnings

Dgraph prints warning messages in the logs when your license is about to expire. If you implement log monitoring, configure alerts for these patterns.

**Before expiry:**

```sh
Your enterprise license will expire in 6 days from now. To continue using enterprise features after 6 days from now, apply a valid license. To get a new license, contact us at https://dgraph.io/contact.
```

**After expiry:**

```sh
Your enterprise license has expired and enterprise features are disabled. To continue using enterprise features, apply a valid license. To receive a new license, contact us at https://dgraph.io/contact.
```

[dcl]: https://github.com/dgraph-io/dgraph/blob/main/licenses/DCL.txt

