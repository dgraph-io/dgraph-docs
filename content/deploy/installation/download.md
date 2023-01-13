+++
date = "2017-03-20T22:25:17+11:00"
title = "Download"
weight = 1
[menu.main]
    parent = "installation"
+++

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

## Install from Source

{{% notice "note" %}}
You can build the Ratel UI from source separately following its build
[instructions](https://github.com/dgraph-io/ratel/blob/master/INSTRUCTIONS.md).
Ratel UI is distributed via Dgraph releases using any of the download methods
listed above. You can also use https://play.dgraph.io/ to run Ratel.
{{% /notice %}}

If you want to install from source, install Go 1.13+ or later and the following dependencies:

#### Ubuntu

```bash
sudo apt-get update
sudo apt-get install build-essential
```

#### macOS

As a prerequisite, first install [XCode](https://apps.apple.com/us/app/xcode/id497799835?mt=12) (or the [XCode Command-line Tools](https://developer.apple.com/downloads/)) and [Homebrew](https://brew.sh/).

Next, install the required dependencies:

```bash
brew update
brew install jemalloc go
```

### Build and Install

Then clone the Dgraph repository and use `make install` to install the Dgraph binary in the directory named by the GOBIN environment variable, which defaults to $GOPATH/bin or $HOME/go/bin if the GOPATH environment variable is not set. 


```bash
git clone https://github.com/dgraph-io/dgraph.git
cd dgraph
make install
```
