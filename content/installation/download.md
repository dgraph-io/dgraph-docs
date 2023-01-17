+++
date = "2017-03-20T22:25:17+11:00"
title = "Download"
weight = 1
[menu.main]
    parent = "installation"
+++

{{% notice "tip" %}}
If you are new to Dgraph, the easiest way to get Dgraph up and running is using the [Dgraph Cloud](https://cloud.dgraph.io/) or to use Dgraph standalone Docker image.
{{% /notice %}}



## Options

You can obtain Dgraph binary for the latest version as well as previous releases using automatic install script, manual download, through Docker images  or by building the binary from the open source code.


{{% tabs %}} {{< tab "Docker" >}}
1. Install Docker.

1. Pull the latest Dgraph image using docker:
   ```sh
      docker pull dgraph/dgraph:{{< version >}}
   ```
1. Verify that the image is downloaded:

   ```sh
      docker images
    ```
{{< /tab >}} 

{{% tab "Automatic" %}}

1. Download the Dgraph installation script to install Dgraph automatically:
   ```sh
      curl https://get.dgraph.io -sSf | bash
   ```   

1. Verify that it works fine, by running:
    ```
     dgraph version
    ```
   For more information about the various installation scripts that you can use, see [install scripts](https://github.com/dgraph-io/Install-Dgraph).   
{{< /tab >}}
{{% tab "Manual" %}}
If you don't want to follow the automatic installation method, you could manually download the appropriate tar for your platform from **[Dgraph releases](https://github.com/dgraph-io/dgraph/releases)**. After downloading the tar for your platform from Github, extract the binary to `/usr/local/bin` like so.

1. Download the installation file:
    ```
      $ sudo tar -C /usr/local/bin -xzf dgraph-linux-amd64-VERSION.tar.gz
    ```
1. Verify that it works fine, by running:
     ```
     dgraph version
     ```     
{{% /tab %}} {{% /tabs %}}


## Install from Source

To install from source, install Go 1.13+ or later and the related dependencies:

**Ubuntu**
```bash
sudo apt-get update
sudo apt-get install build-essential
```

### Build and Install

1. Clone the Dgraph repository in a directory named `<INSTALL>`.
1. Set `<INSTALL>` in `GOBIN` environment variable, which defaults to `$GOPATH/bin`. 
1. Use `make install` to install the Dgraph binary in the directory. 
   If the `GOPATH` environment variable is not set the binaries are installed in or `$HOME/go/bin`. 
   
```bash
git clone https://github.com/dgraph-io/dgraph.git
cd dgraph
make install
```
{{% notice "note" %}}
You can build the Ratel UI from source separately following its build
[instructions](https://github.com/dgraph-io/ratel/blob/master/INSTRUCTIONS.md).
Ratel UI is distributed via Dgraph releases using any of the download methods
listed above. You can also use https://play.dgraph.io/ to run Ratel.
{{% /notice %}}

