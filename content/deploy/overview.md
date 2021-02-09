+++
date = "2021-02-08"
title = "Download"
description = "Deploy and manage Dgraph database in your physical or cloud infrastructure."
weight = 1
[menu.main]
    parent = "deploy"
+++

You can deploy and manage Dgraph database in a variety of self-managed deployment scenarios, including:

* Running Dgraph on your on-premises infrastructure (physical servers)
* Running Dgraph on your cloud infrastructure (AWS, GCP and Azure)

This section focuses exclusively on deployment and management for these self-managed
scenarios. To learn about fully-managed options that let you focus on
building apps and websites, rather than managing infrastructure, see the 
[Dgraph cloud services docs](https://dgraph.io/docs/slash-graphql/), or 
[Try Slash GraphQL](https://slash.dgraph.io/).

Dgraph runs on two types of server nodes, even when you are doing a proof-of-concept
deployment using a single-host setup:

* Dgraph Alpha database server: The Dgraph Alpha server nodes in your deployment host and serve data. These nodes also host an `/admin` HTTP and GRPC endpoint that can
be used for data and node administration tasks such as backup, export, draining,
and shutdown.
* Dgraph Zero management server: The Dgraph Zero nodes in your deployment control
the nodes in your Dgraph cluster. Dgraph Zero automatically moves data between different Dgraph Alpha instances based on the volume of data served by each Alpha instance.





{{% notice "tip" %}}
For a single server setup, recommended for new users, please see [Get Started]({{< relref "get-started/index.md" >}}) page.
{{% /notice %}}

## Docker

```sh
docker pull dgraph/dgraph:{{< version >}}

# You can test that it worked fine, by running:
docker run -it dgraph/dgraph:{{< version >}} dgraph
```

## Automatic download

Running

```sh
curl https://get.dgraph.io -sSf | bash

# Test that it worked fine, by running:
dgraph
```

would install the `dgraph` binary into your system.

Other installation options:

> Add `-s --` before the flags.()
`-y | --accept-license`: Automatically agree to the terms of the Dgraph Community License (default: "n").

`-s | --systemd`: Automatically create Dgraph's installation as Systemd services (default: "n").

`-v | --version`: Choose Dgraph's version manually (default: The latest stable release, you can do tag combinations e.g {{< version >}}-beta1 or -rc1).

>Installing Dgraph and requesting the automatic creation of systemd service. e.g:

```sh
curl https://get.dgraph.io -sSf | bash -s -- --systemd
```

Using Environment variables:

`ACCEPT_LICENSE`: Automatically agree to the terms of the Dgraph Community License (default: "n").

`INSTALL_IN_SYSTEMD`: Automatically create Dgraph's installation as Systemd services (default: "n").

`VERSION`: Choose Dgraph's version manually (default: The latest stable release).

```sh
curl https://get.dgraph.io -sSf | VERSION={{< version >}}-beta1 bash
```

{{% notice "note" %}}
Be aware that using this script will overwrite the installed version and can lead to compatibility problems. For example, if you were using version v1.0.5 and forced the installation of {{< version >}}-Beta, the existing data won't be compatible with the new version. The data must be [exported]({{< relref "deploy/dgraph-administration.md#exporting-database" >}}) before running this script and reimported to the new cluster running the updated version.
{{% /notice %}}

## Manual download [optional]

If you don't want to follow the automatic installation method, you could manually download the appropriate tar for your platform from **[Dgraph releases](https://github.com/dgraph-io/dgraph/releases)**. After downloading the tar for your platform from Github, extract the binary to `/usr/local/bin` like so.

```sh
# For Linux
$ sudo tar -C /usr/local/bin -xzf dgraph-linux-amd64-VERSION.tar.gz

# For Mac
$ sudo tar -C /usr/local/bin -xzf dgraph-darwin-amd64-VERSION.tar.gz

# Test that it worked fine, by running:
dgraph
```

## Building from Source

{{% notice "note" %}}
You can build the Ratel UI from source separately following its build
[instructions](https://github.com/dgraph-io/ratel/blob/master/INSTRUCTIONS.md).
Ratel UI is distributed via Dgraph releases using any of the download methods
listed above.
{{% /notice %}}

Make sure you have [Go](https://golang.org/dl/) v1.11+ installed.

You'll need the following dependencies to install Dgraph using `make`:
```bash
sudo apt-get update
sudo apt-get install gcc make
```

After installing Go, run
```sh
# This should install dgraph binary in your $GOPATH/bin.

git clone https://github.com/dgraph-io/dgraph.git
cd ./dgraph
make install
```

If you get errors related to `grpc` while building them, your
`go-grpc` version might be outdated. We don't vendor in `go-grpc`(because it
causes issues while using the Go client). Update your `go-grpc` by running.
```sh
go get -u -v google.golang.org/grpc
```
