+++
date = "2017-03-20T22:25:17+11:00"
title = "Highly Available Cluster Setup"
weight = 4
[menu.main]
    parent = "kubernetes"
+++

You can run three Dgraph Alpha servers and three Dgraph Zero servers in a highly available cluster setup. For a highly available setup, start the Dgraph Zero server  with `--replicas 3` flag, so that all data is replicated on three Alpha servers and forms one Alpha group. You can install a highly available cluster using:
*  [dgraph-ha.yaml](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/kubernetes/dgraph-ha/dgraph-ha.yaml) file
*  Helm charts.

### Install a highly avaiable Dgraph cluster using YAML or Helm

{{% tabs %}} {{< tab "YAML" >}}
#### Before you begin:

* Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
* Ensure that you have a production-ready Kubernetes cluster with atleast three worker nodes running in a cloud provider of your choice.
* (Optional) To run Dgraph Alpha with TLS, see [TLS Configuration]({{< relref "tls-configuration.md" >}}).

#### Installing a highly available Dgraph cluster

1.  Verify that you are able to access the nodes in the Kubernetes cluster:

    ```bash
    kubectl get nodes
    ```

    An output similar to this appears:

     ```bash
       NAME                                          STATUS   ROLES    AGE   VERSION
      <aws-ip-hostname>.<region>.compute.internal   Ready    <none>   1m   v1.15.11-eks-af3caf
      <aws-ip-hostname>.<region>.compute.internal   Ready    <none>   1m   v1.15.11-eks-af3caf
      <aws-ip-hostname>.<region>.compute.internal   Ready    <none>   1m   v1.15.11-eks-af3caf
      ```
    After your Kubernetes cluster is up, you can use [dgraph-ha.yaml](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/kubernetes/dgraph-ha/dgraph-ha.yaml) to start the cluster. 

1.  Start a StatefulSet that creates Pods with `Zero`, `Alpha`, and `Ratel UI`:
    
     ```bash
     kubectl create --filename https://raw.githubusercontent.com/dgraph-io/dgraph/main/contrib/config/kubernetes/dgraph-ha/dgraph-ha.yaml
     ```
    An output similar to this appears:

      ```bash
      service/dgraph-zero-public created
      service/dgraph-alpha-public created
      service/dgraph-ratel-public created
      service/dgraph-zero created
      service/dgraph-alpha created
      statefulset.apps/dgraph-zero created
      statefulset.apps/dgraph-alpha created
      deployment.apps/dgraph-ratel created
      ```
1. Confirm that the Pods were created successfully.

    ```bash
    kubectl get pods
    ```
    An output similar to this appears:
   
     ```bash
      NAME                  READY   STATUS    RESTARTS   AGE
     dgraph-alpha-0        1/1     Running   0          6m24s
     dgraph-alpha-1        1/1     Running   0          5m42s
     dgraph-alpha-2        1/1     Running   0          5m2s
     dgraph-ratel-<pod-id> 1/1     Running   0          6m23s
     dgraph-zero-0         1/1     Running   0          6m24s
     dgraph-zero-1         1/1     Running   0          5m41s
     dgraph-zero-2         1/1     Running   0          5m6s
     ```
    You can check the logs for the Pod using `kubectl logs --follow <POD_NAME>`.. 

1. Port forward from your local machine to the Pod:

    ```bash
       kubectl port-forward service/dgraph-alpha-public 8080:8080
       kubectl port-forward service/dgraph-ratel-public 8000:8000
    ```
1.  Go to `http://localhost:8000` to access Dgraph using the Ratel UI.

{{% notice "note" %}} You can also access the service on its External IP address.{{% /notice %}}

#### Deleting highly available Dgraph resources

Delete all the resources using:

```sh
kubectl delete --filename https://raw.githubusercontent.com/dgraph-io/dgraph/main/contrib/config/kubernetes/dgraph-ha/dgraph-ha.yaml
kubectl delete persistentvolumeclaims --selector app=dgraph-zero
kubectl delete persistentvolumeclaims --selector app=dgraph-alpha
```
{{< /tab >}} 
{{< tab "Helm" >}}

#### Before you begin

* Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
* Ensure that you have a production-ready Kubernetes cluster with atleast three worker nodes running in a cloud provider of your choice.
* Install [Helm](https://helm.sh/docs/intro/install/).
* (Optional) To run Dgraph Alpha with TLS, see [TLS Configuration]({{< relref "tls-configuration.md" >}}).

#### Installing a highly available Dgraph cluster using Helm

1.  Verify that you are able to access the nodes in the Kubernetes cluster:

    ```bash
    kubectl get nodes
    ```

    An output similar to this appears:

     ```bash
       NAME                                          STATUS   ROLES    AGE   VERSION
      <aws-ip-hostname>.<region>.compute.internal   Ready    <none>   1m   v1.15.11-eks-af3caf
      <aws-ip-hostname>.<region>.compute.internal   Ready    <none>   1m   v1.15.11-eks-af3caf
      <aws-ip-hostname>.<region>.compute.internal   Ready    <none>   1m   v1.15.11-eks-af3caf
      ```
     After your Kubernetes cluster is up and running, you can use of the [Dgraph Helm chart](https://github.com/dgraph-io/charts/) to install a highly avaiable Dgraph cluster

1.  Add the Dgraph helm repository::
    
     ```bash
     helm repo add dgraph https://charts.dgraph.io
     ```
1. Install the chart with `<RELEASE-NAME>`:

    ```bash
    helm install <RELEASE-NAME> dgraph/dgraph
    ```

    You can also specify the version using:
    ```bash
       helm install <RELEASE-NAME> dgraph/dgraph --set image.tag="{{< version >}}"
    ```
    When configuring the Dgraph image tag, be careful not to use `latest` or `main` in a production environment. These tags may have the Dgraph version change, causing a mixed-version Dgraph cluster that can lead to an outage and potential data loss.
        
    An output similar to this appears:
   
        ```bash
        NAME: <RELEASE-NAME>
        LAST DEPLOYED: Wed Feb  1 21:26:32 2023
        NAMESPACE: default
        STATUS: deployed
        REVISION: 1
        TEST SUITE: None
        NOTES:
        1. You have just deployed Dgraph, version 'v21.12.0'.
      
           For further information:
            * Documentation: https://dgraph.io/docs/
            * Community and Issues: https://discuss.dgraph.io/   
        2. Get the Dgraph Alpha HTTP/S endpoint by running these commands.
           export ALPHA_POD_NAME=$(kubectl get pods --namespace default --selector "statefulset.kubernetes.io/pod-name=<RELEASE-NAME>-dgraph-alpha-0,release=<RELEASE-NAME>-dgraph" --output jsonpath="{.items[0].metadata.name}")
           echo "Access Alpha HTTP/S using http://localhost:8080"
           kubectl --namespace default port-forward $ALPHA_POD_NAME 8080:8080
      
          NOTE: Change "http://" to "https://" if TLS was added to the Ingress, Load Balancer, or Dgraph Alpha service.
        ```
1. Get the name of the Pods in the cluster using `kubectl get pods`:
    ```bash
       NAME                          READY   STATUS    RESTARTS   AGE
      <RELEASE-NAME>-dgraph-alpha-0   1/1     Running   0          4m48s
      <RELEASE-NAME>-dgraph-alpha-1   1/1     Running   0          4m2s
      <RELEASE-NAME>-dgraph-alpha-2   1/1     Running   0          3m31s
      <RELEASE-NAME>-dgraph-zero-0    1/1     Running   0          4m48s
      <RELEASE-NAME>-dgraph-zero-1    1/1     Running   0          4m10s
      <RELEASE-NAME>-dgraph-zero-2    1/1     Running   0          3m50s

1. Get the Dgraph Alpha HTTP/S endpoint by running these commands:
    ```bash
        export ALPHA_POD_NAME=$(kubectl get pods --namespace default --selector "statefulset.kubernetes.io/pod-name=<RELEASE-NAME>-dgraph-alpha-0,release=<RELEASE-NAME>-dgraph" --output jsonpath="{.items[0].metadata.name}")
        echo "Access Alpha HTTP/S using http://localhost:8080"
        kubectl --namespace default port-forward $ALPHA_POD_NAME 8080:8080
    ```
#### Deleting the resources from the cluster

1. Delete the Helm deployment using:

   ```sh
     helm delete my-release
   ```
2. Delete associated Persistent Volume Claimss:

   ```sh
   kubectl delete pvc --selector release=my-release
   ```
{{< /tab >}}    
{{% /tabs %}}


### Dgraph configuration files

You can create a Dgraph [Config]({{< relref "deploy/config.md" >}}) files for Alpha server and Zero server with Helm chart configuration values, `<MY-CONFIG-VALUES>`. For more information about the values, see the latest [configuration settings](https://github.com/dgraph-io/charts/blob/master/charts/dgraph/README.md#configuration).

1. Open an editor of your choice and create a config file named `<MY-CONFIG-VALUES>.yaml`:

```yaml
# <MY-CONFIG-VALUES>.yaml
alpha:
  configFile:
    config.yaml: |
      alsologtostderr: true
      badger:
        compression_level: 3
        tables: mmap
        vlog: mmap
      postings: /dgraph/data/p
      wal: /dgraph/data/w
zero:
  configFile:
    config.yaml: |
      alsologtostderr: true
      wal: /dgraph/data/zw
```

2. Change to the director in which you created `<MY-CONFIG-VALUES>`.yaml and then install with Alpha and Zero configuration using:

```sh
helm install <RELEASE-NAME> dgraph/dgraph --values <MY-CONFIG-VALUES>.yaml
```

### Exposing Alpha and Ratel Services

By default Zero and Alpha services are exposed only within the Kubernetes cluster as
Kubernetes service type `ClusterIP`.

In order to expose the Alpha service and Ratel service publicly you can use Kubernetes service type `LoadBalancer` or an Ingress resource.

{{% tabs %}} {{< tab "LoadBalancer" >}}

##### Public Internet

To use an external load balancer, set the service type to `LoadBalancer`. 

{{% notice "note" %}}For security purposes we recommend limiting access to any public endpoints, such as using a white list.{{% /notice %}}

1.  To expose Alpha service to the Internet use:

```sh
helm install <RELEASE-NAME> dgraph/dgraph --set alpha.service.type="LoadBalancer"
```

2.  To expose Alpha and Ratel services to the Internet use:

```sh
helm install <RELEASE-NAME> dgraph/dgraph --set alpha.service.type="LoadBalancer" --set ratel.service.type="LoadBalancer"
```

##### Private Internal Network

An external load balancer can be configured to face internally to a private subnet rather the public Internet.  This way it can be accessed securely by clients on the same network, through a VPN, or from a jump server. In Kubernetes, this is often configured through service annotations by the provider.  Here's a small list of annotations from cloud providers:

|Provider    | Documentation Reference   | Annotation |
|------------|---------------------------|------------|
|AWS         |[Amazon EKS: Load Balancing](https://docs.aws.amazon.com/eks/latest/userguide/load-balancing.html)|`service.beta.kubernetes.io/aws-load-balancer-internal: "true"`|
|Azure       |[AKS: Internal Load Balancer](https://docs.microsoft.com/azure/aks/internal-lb)|`service.beta.kubernetes.io/azure-load-balancer-internal: "true"`|
|Google Cloud|[GKE: Internal Load Balancing](https://cloud.google.com/kubernetes-engine/docs/how-to/internal-load-balancing)|`cloud.google.com/load-balancer-type: "Internal"`|


As an example, using Amazon [EKS](https://aws.amazon.com/eks/) as the provider.

1. Create a Helm chart configuration values file `<MY-CONFIG-VALUES>`.yaml file: 

```yaml
# <MY-CONFIG-VALUES>.yaml
alpha:
  service:
    type: LoadBalancer
    annotations:
      service.beta.kubernetes.io/aws-load-balancer-internal: "true"
ratel:
  service:
    type: LoadBalancer
    annotations:
      service.beta.kubernetes.io/aws-load-balancer-internal: "true"
```

1. To expose Alpha and Ratel services privately, use:

```sh
helm install <RELEASE-NAME> dgraph/dgraph --values <MY-CONFIG-VALUES>.yaml
```
{{% /tab %}}
{{% tab "Ingress Resource" %}}

You can expose Alpha and Ratel using an [ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) resource that can route traffic to service resources.  Before using this option you may need to install an [ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) first, as is the case with [AKS](https://docs.microsoft.com/azure/aks/) and [EKS](https://aws.amazon.com/eks/), while in the case of [GKE](https://cloud.google.com/kubernetes-engine), this comes bundled with a default ingress controller.  When routing traffic based on the `hostname`, you may want to integrate an addon like [ExternalDNS](https://github.com/kubernetes-sigs/external-dns) so that DNS records can be registered automatically when deploying Dgraph.

As an example, you can configure a single ingress resource that uses [ingress-nginx](https://github.com/kubernetes/ingress-nginx) for Alpha and Ratel services.

1.  Create a Helm chart configuration values file, `<MY-CONFIG-VALUES>`.yaml file:

```yaml
# <MY-CONFIG-VALUES>.yaml
global:
  ingress:
    enabled: false
    annotations:
      kubernetes.io/ingress.class: nginx
    ratel_hostname: "ratel.<my-domain-name>"
    alpha_hostname: "alpha.<my-domain-name>"
```

2. To expose Alpha and Ratel services through an ingress:

```sh
helm install <RELEASE-NAME> dgraph/dgraph --values <MY-CONFIG-VALUES>.yaml
```

You can run `kubectl get ingress` to see the status and access these through their hostname, such as `http://alpha.<my-domain-name>` and `http://ratel.<my-domain-name>`


{{% notice "tip" %}}Ingress controllers will likely have an option to configure access for private internal networks.  Consult documentation from the ingress controller provider for further information.{{% /notice %}}
{{% /tab %}}{{% /tabs %}}

### Upgrading the Helm chart

You can update your cluster configuration by updating the configuration of the
Helm chart. Dgraph is a stateful database that requires some attention on
upgrading the configuration carefully in order to update your cluster to your
desired configuration.

In general, you can use [`helm upgrade`][helm-upgrade] to update the
configuration values of the cluster. Depending on your change, you may need to
upgrade the configuration in multiple steps.

[helm-upgrade]: https://helm.sh/docs/helm/helm_upgrade/

To upgrade to an [HA cluster setup]({{< relref "#ha-cluster-setup-using-kubernetes" >}}): 

1. Ensure that the shard replication setting is more than one and `zero.shardReplicaCount`. For example, set the shard replica flag on the Zero node group to 3,`zero.shardReplicaCount=3`.
2. Run the Helm upgrade command to restart the Zero node group:
   ```sh
   helm upgrade <RELEASE-NAME> dgraph/dgraph [options]
   ```
3. Set the Alpha replica count flag. For example: `alpha.replicaCount=3`.
4. Run the Helm upgrade command again:
   ```sh
   helm upgrade <RELEASE-NAME> dgraph/dgraph [options]
   ```


