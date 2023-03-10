+++
date = "2017-03-20T22:25:17+11:00"
title = "Single Server Cluster Setup"
weight = 2
[menu.main]
    parent = "kubernetes"
+++


You can install a single server Dgraph cluster in Kubernetes.

## Before you begin

* Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
* Ensure that you have a production-ready Kubernetes cluster running in a cloud provider of your choice.
* (Optional) To run Dgraph Alpha with TLS, see [TLS Configuration]({{< relref "deploy/tls-configuration.md" >}}).

## Installing a single server Dgraph cluster

1.  Verify that you are able to access the nodes in the Kubernetes cluster:

    ```bash
    kubectl get nodes
    ```

    An output similar to this appears:

     ```bash
       NAME                                          STATUS   ROLES    AGE   VERSION
       <aws-ip-hostname>.<region>.compute.internal   Ready    <none>   1m   v1.15.11-eks-af3caf
       <aws-ip-hostname>.<region>.compute.internal   Ready    <none>   1m   v1.15.11-eks-af3caf
      ```
    After your Kubernetes cluster is up, you can use [dgraph-single.yaml](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/kubernetes/dgraph-single/dgraph-single.yaml) to start a Zero, Alpha, and Ratel UI services.

1.  Start a StatefulSet that creates a single Pod with `Zero`, `Alpha`, and `Ratel UI`:
    
     ```bash
     kubectl create --filename https://raw.githubusercontent.com/dgraph-io/dgraph/main/contrib/config/kubernetes/dgraph-single/dgraph-single.yaml
     ```
    An output similar to this appears:

      ```bash
      service/dgraph-public created
      statefulset.apps/dgraph created
      ```
1. Confirm that the Pod was created successfully.

    ```bash
    kubectl get pods
    ```
    An output similar to this appears:
   
     ```bash
      NAME       READY     STATUS    RESTARTS   AGE
      dgraph-0   3/3       Running   0          1m
     ```

1.  List the containers running in the Pod `dgraph-0`:
    ```bash
       kubectl get pods dgraph-0 -o jsonpath='{range .spec.containers[*]}{.name}{"\n"}{end}'
    ```
    An output similar to this appears:
    ```bash
       ratel
       zero
       alpha
    ```   
    You can check the logs for the containers in the pod using
    `kubectl logs --follow dgraph-0 <CONTAINER_NAME>`. 

1. Port forward from your local machine to the Pod:

    ```bash
       kubectl port-forward pod/dgraph-0 8080:8080
       kubectl port-forward pod/dgraph-0 8000:8000
    ```
1.  Go to `http://localhost:8000` to access Dgraph using the Ratel UI.

## Deleting Dgraph single server resources

Delete all the resources using:

```sh
kubectl delete --filename https://raw.githubusercontent.com/dgraph-io/dgraph/main/contrib/config/kubernetes/dgraph-single/dgraph-single.yaml
kubectl delete persistentvolumeclaims --selector app=dgraph
```

