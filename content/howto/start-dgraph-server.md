+++
date = ""
title = "Start a Dgraph Server"
weight = 1
[menu.main]
    parent = "howto"
+++
### Get started with self-managed Dgraph

To run Dgraph on your own server, see [instructions for single-node setup]({{< relref "/deploy/single-host-setup" >}})
or [instructions for cluster setup]({{< relref "/deploy/multi-host-setup" >}}).

{{% notice "note" %}}
Dgraph is designed to run on Linux. As of release v21.03, Dgraph no longer
supports installation on Windows or macOS. We recommend using the standalone
Docker image to try out Dgraph on Windows or macOS.
{{% /notice %}}

#### To run Dgraph using the standalone Docker image

1. Download docker: https://www.docker.com/
2. Create a folder to store Dgraph data outside of the container, as follows: `mkdir -p ~/dgraph`
3. Get the Docker standalone image, as follows: `docker pull dgraph/standalone`
4. Run the Dgraph Docker standalone image, as follows:

```sh
  docker run -it -p 5080:5080 -p 6080:6080 -p 8080:8080 -p 9080:9080 -v ~/dgraph:/dgraph --name dgraph dgraph/standalone:{{< version >}}
```  

{{% notice "tip" %}}
To run the Docker standalone image for another version of Dgraph, change `v21.03.0`
in the command shown above to the version number for a previous release, such as `v20.11.0`.
{{% /notice %}}

After following these steps, Dgraph Alpha now runs and listens for HTTP requests
on port 8080, and Ratel listens on port 8000(you can also use https://play.dgraph.io/ to run Ratel).
