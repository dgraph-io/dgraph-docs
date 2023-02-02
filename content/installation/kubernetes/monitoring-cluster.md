+++
date = "2017-03-20T22:25:17+11:00"
title = "Monitoring the Cluster"
weight = 4
[menu.main]
    parent = "kubernetes"
+++



## Monitoring in Kubernetes

Dgraph exposes Prometheus metrics to monitor the state of various components involved in the cluster, including Dgraph Alpha and Zero nodes.

Below are instructions to setup Prometheus monitoring for your cluster. This solution has the following parts:

* [prometheus-operator](https://coreos.com/blog/the-prometheus-operator.html) - a Kubernetes operator to install and configure Prometheus and Alert Manager.
* [Prometheus](https://prometheus.io/) - the service that will scrape Dgraph for metrics
* [AlertManager](https://prometheus.io/docs/alerting/latest/alertmanager/) - the service that will trigger alerts to a service (Slack, PagerDuty, etc) that you specify based on metrics exceeding threshold specified in Alert rules.
* [Grafana](https://grafana.com/) - optional visualization solution that will use Prometheus as a source to create dashboards.

### Installation through Manifests

Follow the below mentioned steps to setup Prometheus monitoring for your cluster.

#### Install Prometheus operator

```sh
kubectl apply --filename https://raw.githubusercontent.com/coreos/prometheus-operator/release-0.34/bundle.yaml
```

Ensure that the instance of `prometheus-operator` has started before continuing.

```sh
$ kubectl get deployments prometheus-operator
NAME                  DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
prometheus-operator   1         1         1            1           3m
```

#### Install Prometheus

* Apply Prometheus manifest present [here](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/monitoring/prometheus/prometheus.yaml).

```sh
$ kubectl apply --filename prometheus.yaml

serviceaccount/prometheus-dgraph-io created
clusterrole.rbac.authorization.k8s.io/prometheus-dgraph-io created
clusterrolebinding.rbac.authorization.k8s.io/prometheus-dgraph-io created
servicemonitor.monitoring.coreos.com/alpha.dgraph-io created
servicemonitor.monitoring.coreos.com/zero-dgraph-io created
prometheus.monitoring.coreos.com/dgraph-io created
```

To view Prometheus UI locally run:

```sh
kubectl port-forward prometheus-dgraph-io-0 9090:9090
```

The UI is accessible at port 9090. Open http://localhost:9090 in your browser to play around.

#### Registering Alerts and Installing Alert Manager

To register alerts from Dgraph cluster with your Prometheus deployment, follow the steps below:

* Create a Kubernetes secret containing alertmanager configuration. Edit the configuration file present [here](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/monitoring/prometheus/alertmanager-config.yaml)
with the required receiver configuration including the slack webhook credential and create the secret.

You can find more information about alertmanager configuration [here](https://prometheus.io/docs/alerting/configuration/).

```sh
$ kubectl create secret generic alertmanager-alertmanager-dgraph-io \
    --from-file=alertmanager.yaml=alertmanager-config.yaml

$ kubectl get secrets
NAME                                            TYPE                 DATA   AGE
alertmanager-alertmanager-dgraph-io             Opaque               1      87m
```

* Apply the [alertmanager](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/monitoring/prometheus/alertmanager.yaml) along with [alert-rules](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/monitoring/prometheus/alert-rules.yaml) manifest
to use the default configured alert configuration. You can also add custom rules based on the metrics exposed by Dgraph cluster similar to [alert-rules](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/monitoring/prometheus/alert-rules.yaml)
manifest.

```sh
$ kubectl apply --filename alertmanager.yaml
alertmanager.monitoring.coreos.com/alertmanager-dgraph-io created
service/alertmanager-dgraph-io created

$ kubectl apply --filename alert-rules.yaml
prometheusrule.monitoring.coreos.com/prometheus-rules-dgraph-io created
```

### Install Using Helm Chart

There are Helm chart values that will install Prometheus, Alert Manager, and Grafana.

You will first need to add the `prometheus-operator` Helm chart:

```bash
$ helm repo add stable https://kubernetes-charts.storage.googleapis.com
```

Afterward you will want to copy the Helm chart values present [here](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/monitoring/prometheus/chart-values/dgraph-prometheus-operator.yaml) and edit them as appropriate, such as adding endpoints, adding alert rules, adjusting alert manager configuration, adding Grafana dashboard, etc.

Once ready, install this with the following:

```bash
$ helm install my-prometheus-release \
  --values dgraph-prometheus-operator.yaml \
  --set grafana.adminPassword='<put-secret-password-here>' \
  stable/prometheus-operator
```

**NOTE**: For security best practices, we want to keep secrets, such as the Grafana password outside of general configuration, so that it is not accidentally checked into anywhere.  You can supply it through the command line, or create a separate `secrets.yaml` that is never checked into a code repository:

```yaml
grafana:
  adminPassword: <put-secret-password-here>
```

Then you can install this in a similar fashion:

```bash
$ helm install my-prometheus-release \
  --values dgraph-prometheus-operator.yaml \
  --values secrets.yaml \
  stable/prometheus-operator
```


### Adding Dgraph Kubernetes Grafana Dashboard

You can use the Grafana dashboard present [here](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/monitoring/grafana/dgraph-kubernetes-grafana-dashboard.json).  You can import this dashboard and select the Prometheus data source installed earlier.

This will visualize all Dgraph Alpha and Zero Kubernetes Pods, using the regex pattern `"/dgraph-.*-[0-9]*$/`.  This can be changed by through the dashboard configuration and selecting the variable Pod.  This might be desirable when you have had multiple releases, and only want to visualize the current release.  For example, if you installed a new release `my-release-3` with the [Dgraph helm chart](https://github.com/dgraph-io/charts/), you can change the regex pattern to `"/my-release-3.*dgraph-.*-[0-9]*$/"` for the Pod variable.

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
of storage volume which you can then attach to your Dgraph pods. You can set up
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

In the event that you need to completely remove a pod (e.g., its disk got
corrupted and data cannot be recovered), you can use the `/removeNode` API to
remove the node from the cluster. With a Kubernetes StatefulSet, you'll need to
remove the node in this order:

1. On the Zero leader, call `/removeNode` to remove the Dgraph instance from
   the cluster (see [More about Dgraph Zero]({{< relref "/deploy/dgraph-zero" >}})). The removed instance will immediately stop
   running. Any further attempts to join the cluster will fail for that instance
   since it has been removed.
2. Remove the PersistentVolumeClaim associated with the pod to delete its data.
   This prepares the pod to join with a clean state.
3. Restart the pod. This will create a new PersistentVolumeClaim to create new
   data directories.

When an Alpha pod restarts in a replicated cluster, it will join as a new member
of the cluster, be assigned a group and an unused index from Zero, and receive
the latest snapshot from the Alpha leader of the group.

When a Zero pod restarts, it must join the existing group with an unused index
ID. You set the index ID with the `--raft` superflag's `idx` option. This might
require you to update the StatefulSet configuration.

## Kubernetes and Bulk Loader

You may want to initialize a new cluster with an existing data set such as data
from the [Dgraph Bulk Loader]({{< relref "deploy/fast-data-loading/bulk-loader.md" >}}). You can use [Init
Containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
to copy the data to the pod volume before the Alpha process runs.

See the `initContainers` configuration in
[dgraph-ha.yaml](https://github.com/dgraph-io/dgraph/blob/main/contrib/config/kubernetes/dgraph-ha/dgraph-ha.yaml)
to learn more.
