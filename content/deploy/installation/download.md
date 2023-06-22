+++
date = "2017-03-20T22:25:17+11:00"
title = "Download"
description = "Download the images and source files to build and install for a production-ready Dgraph cluster"
weight = 1
[menu.main]
    parent = "installation"
+++




You can obtain Dgraph binary for the latest version as well as previous releases using automatic install script, manual download, through Docker images  or by building the binary from the open source code.


{{% tabs %}} {{< tab "Docker" >}}
1. Install Docker.

1. Pull the latest Dgraph image using docker:
   ```sh
      docker pull dgraph/dgraph:latest
   ```
   To set up a [learning environment]({{< relref "single-host-setup.md" >}}), you may pull the [Dgraph standalone](https://hub.docker.com/r/dgraph/standalone) image :

   ```sh
      docker pull dgraph/standalone:latest
   ```
1. Verify that the image is downloaded:

   ```sh
      docker images
    ```



{{< /tab >}}

{{% tab "Installer" %}}
On a Linux system, you can get the binary using the automatic script:
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
{{% tab "Binary" %}}
On a Linux system, you can download a tar file and install manually.
Download the appropriate tar for your platform from **[Dgraph releases](https://github.com/dgraph-io/dgraph/releases)**. After downloading the tar for your platform from Github, extract the binary to `/usr/local/bin` like so.

1. Download the installation file:
    ```
      $ sudo tar -C /usr/local/bin -xzf dgraph-linux-amd64-VERSION.tar.gz
    ```
1. Verify that it works fine, by running:
     ```
     dgraph version
     ```     
{{% /tab %}}
{{% tab "Source" %}}
You can also build **Dgraph** and **Ratel UI** from the source code by following the instructions from [Contributing to Dgraph](https://github.com/dgraph-io/dgraph/blob/master/CONTRIBUTING.md) or [Building and running Ratel](https://github.com/dgraph-io/ratel/blob/master/INSTRUCTIONS.md).
{{% /tab %}}{{% /tabs %}}
