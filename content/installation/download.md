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


You can obtain Dgraph binary for the latest version as well as previous releases using automatic install script, manual download, through Docker images  or by building the binary from the open source code.


{{% tabs %}} {{< tab "Docker" >}}
1. Install Docker.

1. Pull the latest Dgraph image using docker:
   ```sh
      docker pull dgraph/dgraph:latest
   ```
1. Verify that the image is downloaded:

   ```sh
      docker images
    ```
{{< /tab >}} 

{{% tab "Automatic" %}}
On linux system, you can get the binary using the automatic script:
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
On linux system, you can download a tar file and install manually. 
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
You can also build **Dgraph** and **Ratel UI** from the source code by following the instructions from [Contributing to Dgraph](https://github.com/dgraph-io/dgraph/blob/master/CONTRIBUTING.md) or [Building and running ratel](https://github.com/dgraph-io/ratel/blob/master/INSTRUCTIONS.md).
{{% /tab %}}{{% /tabs %}}

