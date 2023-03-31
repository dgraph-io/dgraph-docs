+++
date = "2017-03-20T22:25:17+11:00"
title = "Learning Environment"
weight = 3
[menu.main]
    parent = "installation"
+++

To learn about Dgraph and the components, you can install and run Dgraph cluster on a single host using Docker, Docker Compose, or Dgraph command line.

{{% tabs %}} {{< tab "Docker" >}}

Dgraph cluster can be setup running as containers on a single host.
{{% notice "note" %}}
To evaluate Dgraph on Windows and macOS use the [standalone Docker image]({{<relref "dgraph-overview#to-run-dgraph-using-the-standalone-docker-image">}}).
{{% /notice %}}

#### Before you begin

Ensure that you have installed:
 * Docker [Desktop](https://docs.docker.com/desktop/) (required for windows or mac)
 * Docker [Engine](https://docs.docker.com/engine/install/)


#### Launch a Dgraph standalone cluster using Docker
1.  Select a name `<CONTAINER_NAME>` for you Docker container and create a directory `<GRAPH_DATA_PATH>` that will hold the Dgraph data on your local file system.
1.  Run a container with the dgraph/standalone image:
    ```sh
       docker run --name <CONTAINER_NAME> -d -p "8080:8080" -p "9080:9080" -v <DGRAPH_DATA_PATH>:/dgraph dgraph/standalone:latest
    ```
1. Optionally launch [Ratel UI]({{< relref "ratel/overview.md" >}}) using the dgraph/ratel docker image :
    ``` sh
    docker run --name ratel  -d -p "8000:8000"  dgraph/ratel:latest
    ```
You can now use Ratel UI on your browser at localhost:8000 and connect to you Dgraph cluster at localhost:8080
#### Setup a Dgraph cluster on a single host using Docker

1. Get the `<IP_ADDRESS>` of the host using:
   ```sh
      ip addr  # On Arch Linux
      ifconfig # On Ubuntu/Mac
   ```
1. Pull the latest Dgraph image using docker:
   ```sh
      docker pull dgraph/dgraph:latest
   ```
1. Verify that the image is downloaded:

   ```sh
      docker images
    ```   
1. Create a `<DGRAPH_NETWORK>` using:
    ```sh
       docker network create <DGRAPH_NETWORK>
    ```
1.  Create a directory `<ZERO_DATA>`to store data for <abbr title="Zero nodes control the Dgraph cluster. It assigns Alpha nodes to groups, re-balances data between groups, handles transaction timestamp and UID assignment.">Dgraph Zero</abbr> and run the container:
    ```sh
       mkdir ~/<ZERO> # Or any other directory where data should be stored.

       docker run -it -p 5080:5080 --network <DGRAPH_NETWORK> -p 6080:6080 -v ~/<ZERO_DATA>:/dgraph dgraph/dgraph:latest dgraph zero --my=<IP_ADDRESS>:5080
    ```
1.  Create a directory `<ALPHA_DATA_1>` to store for <abbr title="Alpha nodes host predicates and indexes. You can scale Dgraph horizontally by adding more Alphas.">Dgraph Alpha
</abbr> and run the container:
    ```sh
     mkdir ~/<ALPHA_DATA_1> # Or any other directory where data should be stored.

     docker run -it -p 7080:7080 --network <DGRAPH_NETWORK> -p 8080:8080 -p 9080:9080 -v ~/<ALPHA_DATA_1>:/dgraph dgraph/dgraph:latest dgraph alpha --zero=<IP_ADDRESS>:5080 --my=<IP_ADDRESS>:7080
    ```
1.  Create a directory `<ALPHA_DATA_2>` to store for the second <abbr title="Alpha nodes host predicates and indexes. You can scale Dgraph horizontally by adding more Alphas.">Dgraph Alpha
</abbr> and run the container:
    ```sh
       mkdir ~/<ALPHA_DATA_2> # Or any other directory where data should be stored.

       docker run -it -p 7081:7081 --network <DGRAPH_NETWORK> -p 8081:8081 -p 9081:9081 -v ~/<ALPHA_DATA_2>:/dgraph dgraph/dgraph:{{< version >}} dgraph alpha --zero=<IP_ADDRESS>:5080 --my=<IP_ADDRESS>:7081  -o=1
    ```
    To override the default ports for the second Alpha use `-o`.    
1.   Connect the Dgraph cluster that are running using https://play.dgraph.io/. For information about connecting, see [Ratel UI]({{< relref "ratel/connection.md" >}}).     

{{< /tab >}}
{{< tab "Dgraph Command Line" >}}

You can run Dgraph directly on a single Linux host.

#### Before you begin

Ensure that you have:
* Installed [Dgraph]({{< relref "download.md" >}}) on the Linux host.
* Made a note of the `<IP_ADDRESS>` of the host.

#### Using Dgraph Command Line
You can start Dgraph on a single host using the dgraph command line.

1. Run Dgraph zero
   ```sh
      dgraph zero --my=<IP_ADDRESS>:5080
   ```
   The `--my` flag is the connection that Dgraph alphas dial to talk to zero. So, the port `5080` and the IP address must be visible to all the Dgraph alphas. For all other various flags, run `dgraph zero --help`.

1. Run two Dgraph alpha nodea:
   ```sh
      dgraph alpha --my=<IP_ADDRESS>:7080 --zero=localhost:5080
      dgraph alpha --my=<IP_ADDRESS>:7081 --zero=localhost:5080 -o=1
   ```
   Dgraph alpha nodes use two directories to persist data and [WAL logs]({{< relref "consistency-model.md" >}}), and these directories must be different for each alpha if they are running on the same host. You can use `-p` and `-w` to change the location of the data and WAL directories.To learn more about other flags, run `dgraph alpha --help`.

1. Connect the Dgraph cluster that are running using https://play.dgraph.io/. For information about connecting, see [Ratel UI]({{< relref "ratel/connection.md" >}}).

{{{< /tab >}}
{{< tab "Docker Compose" >}}

You can install Dgraph using the Docker Compose on a system hosted on any of the cloud provider.

#### Before you begin

   * Ensure that you have installed Docker [Compose](https://docs.docker.com/compose/).
   * IP address of the system on cloud `<CLOUD_IP_ADDRESS>`.
   * IP address of the local host `<IP_ADDRESS>`.

#### Using Docker Compose

1. Download the Dgraph `docker-compose.yml` file:

       wget https://github.com/dgraph-io/dgraph/raw/main/contrib/config/docker/docker-compose.yml

   By default only the localhost IP 127.0.0.1 is allowed. When you run Dgraph on Docker, the containers are assigned IPs and those IPs need to be added to the allowed list.

1. Add a list of IPs allowed for Dgraph so that you can create the schema. Use an     editor of your choice and add the `<IP_ADDRESS>` of the local host in `docker-compose.yml` file:
    ```txt
    # This Docker Compose file can be used to quickly boot up Dgraph Zero
    # and Alpha in different Docker containers.
    # It mounts /tmp/data on the host machine to /dgraph within the
    # container. You will need to change /tmp/data to a more appropriate location.
    # Run `docker-compose up` to start Dgraph.
   version: "3.2"
   services:
      zero:
        image: dgraph/dgraph:latest
        volumes:
          - /tmp/data:/dgraph
        ports:
          - 5080:5080
          - 6080:6080
        restart: on-failure
        command: dgraph zero --my=zero:5080
      alpha:
        image: dgraph/dgraph:latest
        volumes:
          - /tmp/data:/dgraph
        ports:
          - 8080:8080
          - 9080:9080
        restart: on-failure
        command: dgraph alpha --my=alpha:7080 --zero=zero:5080 --security whitelist=<IP_ADDRESS>
      ratel:
        image: dgraph/ratel:latest
        ports:
          - 8000:8000

      ```

1. Run the `docker-compose` command to start the Dgraph services in the docker container:

       sudo docker-compose up

   After Dgraph is installed on Docker, you can view the images and the containers running in Docker for Dgraph.

1. View the containers running for Dgraph using:

       sudo docker ps -a

    An output similar to the following appears:

   ```bash
   CONTAINER ID   IMAGE                  COMMAND                  CREATED
   4b67157933b6   dgraph/dgraph:latest   "dgraph zero --my=ze…"   2 days ago
   3faf9bba3a5b   dgraph/ratel:latest    "/usr/local/bin/dgra…"   2 days ago
   a6b5823b668d   dgraph/dgraph:latest   "dgraph alpha --my=a…"   2 days ago
   ```

1. To access the <abbr title="Ratel is an open source tool for data visualization and cluster management that’s designed to work with Dgraph and DQL.">Ratel UI</abbr> for queries, mutations, and altering schema, open your web browser and navigate to `http://<CLOUD_IP_ADDRESS>:8000`.
1. Click **Launch Latest** to access the latest stable release of Ratel UI.
1. In the **Dgraph Server Connection** dialog that set the **Dgraph server URL** as `http://<CLOUD_IP_ADDRESS>:8080`
1. Click **Connect** . The connection health appears green.
1. Click **Continue** to query or run mutations.
{{% /tab %}}{{% /tabs %}}
