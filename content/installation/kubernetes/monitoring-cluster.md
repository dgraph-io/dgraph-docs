+++
date = "2017-03-20T22:25:17+11:00"
title = "Monitoring the Cluster"
weight = 4
[menu.main]
    parent = "kubernetes"
+++

## Monitoring the Kubernetes Cluster

Dgraph exposes Prometheus metrics to monitor the state of various components involved in the cluster, including Dgraph Alpha and Zero nodes. You can setup Prometheus monitoring for your cluster.

You can use Helm to install [kube-prometheus-stack](https://github.com/prometheus-operator/kube-prometheus) chart. This Helm chart is a collection of Kubernetes manifests, [Grafana](http://grafana.com/) dashboards, [Prometheus rules](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/) combined with scripts to provide monitoring with [Prometheus](https://prometheus.io/) using the [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator). This Helm chart also installs [Grafana](http://grafana.com/), [node_exporter](https://github.com/prometheus/node_exporter), [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics).

### Before you begin:

* Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
* Ensure that you have a production-ready Kubernetes cluster with atleast three worker nodes running in a cloud provider of your choice.
* Install [Helm](https://helm.sh/docs/intro/install/).
* (Optional) To run Dgraph Alpha with TLS, see [TLS Configuration]({{< relref "deploy/tls-configuration.md" >}}).

### Install using Helm Chart

1. Create a `YAML` file named `dgraph-prometheus-operator.yaml` and edit the values as appropriate for adding endpoints, adding alert rules, adjusting alert manager configuration, adding Grafana dashboard, and others. For more information see, [Dgraph helm chart values](https://github.com/dgraph-io/dgraph/tree/main/contrib/config/monitoring/prometheus/chart-values).

   ```yaml
   prometheusOperator:
     createCustomResource: true

   grafana:
     enabled: true
     persistence:
       enabled: true
       accessModes: ["ReadWriteOnce"]
       size: 5Gi
     defaultDashboardsEnabled: true
     service:
       type: ClusterIP
   
   alertmanager:
     service:
       labels:
         app: dgraph-io
     alertmanagerSpec:
       storage:
         volumeClaimTemplate:
           spec:
             accessModes: ["ReadWriteOnce"]
             resources:
               requests:
                 storage: 5Gi
       replicas: 1
       logLevel: debug
     config:
       global:
         resolve_timeout: 2m
       route:
         group_by: ['job']
         group_wait: 30s
         group_interval: 5m
         repeat_interval: 12h
         receiver: 'null'
         routes:
         - match:
             alertname: Watchdog
              receiver: 'null'
       receivers:
       - name: 'null'
   
   prometheus:
     service:
         type: ClusterIP
     serviceAccount:
       create: true
       name: prometheus-dgraph-io
   
     prometheusSpec:
       storageSpec:
         volumeClaimTemplate:
           spec:
             accessModes: ["ReadWriteOnce"]
             resources:
               requests:
                 storage: 25Gi
       resources:
         requests:
           memory: 400Mi
       enableAdminAPI: false

     additionalServiceMonitors:
       - name: zero-dgraph-io
         endpoints:
           - port: http-zero
             path: /debug/prometheus_metrics
         namespaceSelector:
           any: true
         selector:
           matchLabels:
             monitor: zero-dgraph-io
       - name: alpha-dgraph-io
         endpoints:
           - port: http-alpha
             path: /debug/prometheus_metrics
         namespaceSelector:
           any: true
         selector:
           matchLabels:
             monitor: alpha-dgraph-io
   ```
1. Create a `YAML` file named `secrets.yaml` that has the credentials for Grafana.

   ```yaml
   grafana:
     adminPassword: <GRAFANA-PASSWORD>
   ```  

1. Add the `prometheus-operator` Helm chart:

   ```bash
   helm repo add stable https://charts.helm.sh/stable
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   ```

1. Install [kube-prometheus-stack](https://github.com/prometheus-operator/kube-prometheus) with the `<MY-RELEASE-NAME>` in the namescape named `monitoring`:

   ```bash
   helm install <MY-RELEASE-NAME>\                                    
     --values dgraph-prometheus-operator.yaml \
     --values secrets.yaml \
     prometheus-community/kube-prometheus-stack --namespace monitoring
   ```
   An output similar to the following appears:

   ```bash
   NAME: dgraph-prometheus-release
   LAST DEPLOYED: Sun Feb  5 21:35:45 2023
   NAMESPACE: monitoring
   STATUS: deployed
   REVISION: 1
   NOTES:
   kube-prometheus-stack has been installed. Check its status by running:
     kubectl --namespace monitoring get pods -l "release=dgraph-prometheus-release"
   
   Visit https://github.com/prometheus-operator/kube-prometheus instructions on how to create & configure Alertmanager and Prometheus instances using the Operator.
   ```   
1. Check the list of services in the `monitoring` namespace using `kubectl get svc -n monitoring`:

   ```bash
   NAME                                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
   alertmanager-operated                                ClusterIP   None             <none>        9093/TCP,9094/TCP,9094/UDP   29s
   dgraph-prometheus-release-alertmanager               ClusterIP   10.128.239.240   <none>        9093/TCP                     32s
   dgraph-prometheus-release-grafana                    ClusterIP   10.128.213.70    <none>        80/TCP                       32s
   dgraph-prometheus-release-kube-state-metrics         ClusterIP   10.128.139.145   <none>        8080/TCP                     32s
   dgraph-prometheus-release-operator                   ClusterIP   10.128.6.5       <none>        443/TCP                      32s
   dgraph-prometheus-release-prometheus                 ClusterIP   10.128.255.88    <none>        9090/TCP                     32s
   dgraph-prometheus-release-prometheus-node-exporter   ClusterIP   10.128.103.131   <none>        9100/TCP                     32s
   prometheus-operated                                  ClusterIP   None             <none>        9090/TCP                     29s
  
   ```
1. Use `kubectl port-forward svc/dgraph-prometheus-release-prometheus -n monitoring 9090` to access Prometheus at `localhost:9090`.
1. Use `kubectl --namespace monitoring port-forward svc/grafana 3000:80` to access Grafana at `localhost:3000`. 
1. Log in to Grafna using the password that you had set in the `secrets.yaml` file.
1. In the **Dashboards** menu of Grafana, select **Import**.
1. In the **Dashboards/Import dashboard** page copy the contents of the [dgraph-kubernetes-grafana-dashboard.json](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/monitoring/grafana/dgraph-kubernetes-grafana-dashboard.json) file in **Import via panel json** and click **Load**.

    You can visualize all Dgraph Alpha and Zero Kubernetes Pods, using the regex pattern `"/dgraph-.*-[0-9]*$/`. You can change this in the dashboard configuration and select the variable Pod. For example, if you have multiple releases, and only want to visualize the current release named `my-release-3`, change the regex pattern to `"/my-release-3.*dgraph-.*-[0-9]*$/"` in the Pod variable of the dashboard configuration.
    By default, the Prometheus that you installed is configured as the `Datasource` in Grafana. 

## Kubernetes Storage

The Kubernetes configurations in the previous sections were configured to run
Dgraph with any storage type (`storage-class: anything`). On the common cloud
environments like AWS, GCP, and Azure, the default storage type are slow disks
like hard disks or low IOPS SSDs. We highly recommend using faster disks for
ideal performance when running Dgraph.

### Local storage

The AWS storage-optimized i-class instances provide locally attached NVMe-based
SSD storage which provide consistent very high IOPS. The Dgraph team uses
i3.large instances on AWS to test Dgraph.

You can create a Kubernetes `StorageClass` object to provision a specific type
of storage volume which you can then attach to your Dgraph Pods. You can set up
your cluster with local SSDs by using [Local Persistent
Volumes](https://kubernetes.io/blog/2018/04/13/local-persistent-volumes-beta/).
This Kubernetes feature is in beta at the time of this writing (Kubernetes
v1.13.1). You can first set up an EC2 instance with locally attached storage.
Once it is formatted and mounted properly, then you can create a StorageClass to
access it.:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: <your-local-storage-class-name>
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```

Currently, Kubernetes does not allow automatic provisioning of local storage. So
a PersistentVolume with a specific mount path should be created:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: <your-local-pv-name>
spec:
  capacity:
    storage: 475Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete
  storageClassName: <your-local-storage-class-name>
  local:
    path: /data
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - <node-name>
```

Then, in the StatefulSet configuration you can claim this local storage in
.spec.volumeClaimTemplate:

```yaml
kind: StatefulSet
...
 volumeClaimTemplates:
  - metadata:
      name: datadir
    spec:
      accessModes:
      - ReadWriteOnce
      storageClassName: <your-local-storage-class-name>
      resources:
        requests:
          storage: 500Gi
```

You can repeat these steps for each instance that's configured with local
node storage.

### Non-local persistent disks

EBS volumes on AWS and PDs on GCP are persistent disks that can be configured
with Dgraph. The disk performance is much lower than locally attached storage
but can be sufficient for your workload such as testing environments.

When using EBS volumes on AWS, we recommend using Provisioned IOPS SSD EBS
volumes (the io1 disk type) which provide consistent IOPS. The available IOPS
for AWS EBS volumes is based on the total disk size. With Kubernetes, you can
request io1 disks to be provisioned with this config with 50 IOPS/GB using the
`iopsPerGB` parameter:

```
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: <your-storage-class-name>
provisioner: kubernetes.io/aws-ebs
parameters:
  type: io1
  iopsPerGB: "50"
  fsType: ext4
```

Example: Requesting a disk size of 250Gi with this storage class would provide
12.5K IOPS.

## Removing a Dgraph Pod

In the event that you need to completely remove a Pod (e.g., its disk got
corrupted and data cannot be recovered), you can use the `/removeNode` API to
remove the node from the cluster. With a Kubernetes StatefulSet, you'll need to
remove the node in this order:

1. On the Zero leader, call `/removeNode` to remove the Dgraph instance from
   the cluster (see [More about Dgraph Zero]({{< relref "/deploy/dgraph-zero" >}})). The removed instance will immediately stop
   running. Any further attempts to join the cluster will fail for that instance
   since it has been removed.
2. Remove the PersistentVolumeClaim associated with the Pod to delete its data.
   This prepares the Pod to join with a clean state.
3. Restart the Pod. This will create a new PersistentVolumeClaim to create new
   data directories.

When an Alpha Pod restarts in a replicated cluster, it will join as a new member
of the cluster, be assigned a group and an unused index from Zero, and receive
the latest snapshot from the Alpha leader of the group.

When a Zero Pod restarts, it must join the existing group with an unused index
ID. You set the index ID with the `--raft` superflag's `idx` option. This might
require you to update the StatefulSet configuration.

## Kubernetes and Bulk Loader

You may want to initialize a new cluster with an existing data set such as data
from the [Dgraph Bulk Loader]({{< relref "deploy/fast-data-loading/bulk-loader.md" >}}). You can use [Init
Containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
to copy the data to the Pod volume before the Alpha process runs.

See the `initContainers` configuration in
[dgraph-ha.yaml](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/kubernetes/dgraph-ha/dgraph-ha.yaml)
to learn more.
