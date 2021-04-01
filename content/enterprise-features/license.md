+++
date = "2017-03-20T22:25:17+11:00"
title = "License"
weight = 8
[menu.main]
    parent = "enterprise-features"
+++

Dgraph enterprise features are proprietary licensed under the [Dgraph Community
License][dcl]. All Dgraph releases contain proprietary code for enterprise features.
Enabling these features requires an enterprise contract from
[contact@dgraph.io](mailto:contact@dgraph.io) or the [discuss
forum](https://discuss.dgraph.io).

**Dgraph enterprise features are enabled by default for 30 days in a new cluster**.
After the trial period of thirty (30) days, the cluster must obtain a license from Dgraph to
continue using the enterprise features released in the proprietary code.

{{% notice "note" %}}
At the conclusion of your 30-day trial period if a license has not been applied to the cluster,
access to the enterprise features will be suspended. The cluster will continue to operate without
enterprise features.
{{% /notice %}}

When you have an enterprise license key, the license can be applied to the cluster by including it
as the body of a POST request and calling `/enterpriseLicense` HTTP endpoint on any Zero server.

```sh
curl -X POST localhost:6080/enterpriseLicense --upload-file ./licensekey.txt
```

It can also be applied by passing the path to the enterprise license file (using the flag
`--enterprise_license`) to the `dgraph zero` command used to start the server. The second option is
useful when the process needs to be automated.

```sh
dgraph zero --enterprise_license ./licensekey.txt
```

**Warning messages related to license expiry**

Dgraph will print a warning message in the logs when your license is about to expire. If you are planning to implement any log monitoring solution, you may note this pattern and configure suitable alerts for yourself. You can find an example of this message below:

```sh
Your enterprise license will expire in 6 days from now. To continue using enterprise features after 6 days from now, apply a valid license. To get a new license, contact us at https://dgraph.io/contact.
```

Once your license has expired, you will see the following warning message in the logs.

```sh
Your enterprise license has expired and enterprise features are disabled. To continue using enterprise features, apply a valid license. To receive a new license, contact us at https://dgraph.io/contact.
```

[dcl]: https://github.com/dgraph-io/dgraph/blob/master/licenses/DCL.txt
