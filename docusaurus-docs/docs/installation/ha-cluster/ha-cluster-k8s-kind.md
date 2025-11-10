---
title: HA Cluster with Kubernetes using kind
---

This guide walks you through installing a highly available Dgraph cluster on Kubernetes using [kind](https://kind.sigs.k8s.io/) (Kubernetes in Docker). kind is ideal for local development and testing, as it creates multi-node Kubernetes clusters that closely simulate production environments.

## Architecture and Key Benefits

### Cluster Architecture

This setup creates a **highly available Dgraph cluster** with:

- **1 control plane node** - Manages the Kubernetes cluster
- **3 worker nodes** - Run Dgraph workloads
- **3 Dgraph Zero pods** - One per worker node (cluster coordination)
- **3 Dgraph Alpha pods** - One per worker node (data storage and queries)

Each worker node runs exactly one Zero and one Alpha pod, ensuring high availability while maximizing resource efficiency.

### Storage Architecture

For local development, data is mapped from your host machine to the kind cluster:

```
Host Machine (Mac/Linux)          kind Worker Nodes          Dgraph Pods
─────────────────────────          ──────────────────         ────────────
$HOME/dgraph-data/                 /dgraph-data/              /dgraph/
  ├── alpha-0/  ──────────────────>  ├── alpha-0/  ─────────>  alpha-0 pod
  ├── alpha-1/  ──────────────────>  ├── alpha-1/  ─────────>  alpha-1 pod
  └── alpha-2/  ──────────────────>  └── alpha-2/  ─────────>  alpha-2 pod
```

This allows you to directly inspect and experiment with Dgraph's data files, including the `p` folders (posting lists).

### Key Benefits

- **High Availability**: Each Zero and Alpha pod runs on a different node, ensuring fault tolerance
- **Resource Efficiency**: Uses only 3 nodes instead of 6, with one Zero and one Alpha per node
- **Production-Like**: Multi-node setup closely simulates real Kubernetes environments
- **Local Development**: Perfect for testing and development without cloud costs
- **Data Persistence**: Persistent storage ensures data survives pod restarts
- **Direct Data Access**: Local disk mapping allows direct inspection and experimentation with data files

## Prerequisites

Before you begin, ensure you have the following tools installed:

- **Docker** - Running and accessible
- **kubectl** - Kubernetes command-line tool
- **Helm** - Kubernetes package manager
- **kind** - Kubernetes in Docker

### Install Prerequisites

On macOS, you can install these tools using Homebrew:

```bash
brew install kind kubectl helm
```

Verify your installations:

```bash
docker --version
kubectl version --client
helm version
kind --version
```

## Step 1: Create Local Data Directories

Create directories on your host machine for each Alpha pod's data:

```bash
mkdir -p $HOME/dgraph-data/alpha-0
mkdir -p $HOME/dgraph-data/alpha-1
mkdir -p $HOME/dgraph-data/alpha-2
```

**Note:** Use absolute paths (e.g., `/Users/your-username/dgraph-data/alpha-0`). Shell shortcuts like `~` do not work in Kubernetes YAML.

## Step 2: Create kind Cluster with Volume Mounts

Create a kind cluster configuration that mounts your local data directory into all worker nodes.

Create a file named `kind-config.yaml`:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
    extraMounts:
    - hostPath: /Users/your-username/dgraph-data  # Replace with your absolute path
      containerPath: /dgraph-data
  - role: worker
    extraMounts:
    - hostPath: /Users/your-username/dgraph-data  # Replace with your absolute path
      containerPath: /dgraph-data
  - role: worker
    extraMounts:
    - hostPath: /Users/your-username/dgraph-data  # Replace with your absolute path
      containerPath: /dgraph-data
```

**Important:** Replace `/Users/your-username/dgraph-data` with your actual absolute path. You can use:

```bash
echo $HOME/dgraph-data
```

Then create the cluster:

```bash
kind create cluster --config kind-config.yaml
```

**What happens during cluster creation:**
- Docker containers are created for each node (1 control plane + 3 workers)
- Kubernetes control plane components are set up in the control plane node
- Worker nodes join the cluster and become ready
- Your local `dgraph-data` directory is mounted into each worker node at `/dgraph-data`
- A kubectl context named `kind-kind` is automatically created and set as default

### Verify Cluster Creation

Verify that your cluster is running correctly:

```bash
kubectl get nodes
```

Expected output:

```
NAME                 STATUS   ROLES           AGE   VERSION
kind-control-plane   Ready    control-plane   2m    v1.27.x
kind-worker          Ready    <none>          2m    v1.27.x
kind-worker2         Ready    <none>          2m    v1.27.x
kind-worker3         Ready    <none>          2m    v1.27.x
```

All nodes should show `STATUS: Ready`.

## Step 3: Create StorageClass

Create a StorageClass for local persistent volumes:

```bash
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Retain
EOF
```

Verify the StorageClass was created:

```bash
kubectl get storageclass
```

## Step 4: Create PersistentVolumes

Create PersistentVolumes that map to your local directories. Each PV explicitly binds to a specific PVC using `claimRef`:

```bash
kubectl apply -f - <<EOF
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: dgraph-dgraph-alpha-pv-0
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  claimRef:
    namespace: default
    name: datadir-dgraph-dgraph-alpha-0
  hostPath:
    path: /dgraph-data/alpha-0
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: dgraph-dgraph-alpha-pv-1
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  claimRef:
    namespace: default
    name: datadir-dgraph-dgraph-alpha-1
  hostPath:
    path: /dgraph-data/alpha-1
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: dgraph-dgraph-alpha-pv-2
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  claimRef:
    namespace: default
    name: datadir-dgraph-dgraph-alpha-2
  hostPath:
    path: /dgraph-data/alpha-2
EOF
```

**How Pod-to-Folder Binding Works:**

The binding is ensured through a predictable chain:

1. **StatefulSet Pod Naming**: Pods are named `dgraph-dgraph-alpha-0`, `-1`, `-2`
2. **StatefulSet PVC Creation**: The `volumeClaimTemplate` creates PVCs: `datadir-dgraph-dgraph-alpha-0`, `-1`, `-2`
3. **PV claimRef Binding**: Each PV's `claimRef` explicitly names the PVC it should bind to
4. **Complete Chain**: `alpha-0 pod → PVC datadir-dgraph-dgraph-alpha-0 → PV dgraph-dgraph-alpha-pv-0 → /dgraph-data/alpha-0`

The `claimRef` creates an explicit, one-to-one binding ensuring alpha-0 always uses the alpha-0 folder.

Verify the PVs were created:

```bash
kubectl get pv
```

You should see three PVs in `Available` status.

## Step 5: Add Dgraph Helm Repository

Add the official Dgraph Helm chart repository:

```bash
helm repo add dgraph https://charts.dgraph.io
helm repo update
```

Verify the repository was added:

```bash
helm repo list
```

## Step 6: Create Helm Values File

Create a Helm values file for high availability configuration:

```yaml
zero:
  replicaCount: 3
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
            - key: app.kubernetes.io/component
              operator: In
              values: ["zero"]
        topologyKey: kubernetes.io/hostname
  persistence:
    enabled: true
    storageClass: local-storage

alpha:
  replicaCount: 3
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
            - key: app.kubernetes.io/component
              operator: In
              values: ["alpha"]
        topologyKey: kubernetes.io/hostname
  persistence:
    enabled: true
    storageClass: local-storage
```

Save this as `dgraph-ha-values.yaml`.

**Configuration explanation:**
- **`replicaCount: 3`** - Creates 3 replicas of Zero and Alpha pods
- **`podAntiAffinity`** - Ensures no two Zero pods (or Alpha pods) are scheduled on the same node
- **`topologyKey: kubernetes.io/hostname`** - Uses node hostname as the topology domain, spreading pods across nodes
- **`persistence.enabled: true`** - Enables persistent storage for data durability
- **`storageClass: local-storage`** - Uses the pre-created StorageClass for local volumes

## Step 7: Install Dgraph

Install the Dgraph Helm chart with your custom values:

```bash
helm install dgraph dgraph/dgraph -f dgraph-ha-values.yaml
```

Wait for all pods to be ready:

```bash
kubectl wait --for=condition=Ready pod -l component=alpha --timeout=300s
kubectl wait --for=condition=Ready pod -l component=zero --timeout=300s
```

## Step 8: Verify Installation

### Check Pod Status

Verify that all Dgraph pods are running and distributed across nodes:

```bash
kubectl get pods -o wide
```

Expected output:

```
NAME               READY   STATUS    NODE            AGE
dgraph-alpha-0     1/1     Running   kind-worker      2m
dgraph-alpha-1     1/1     Running   kind-worker2    2m
dgraph-alpha-2     1/1     Running   kind-worker3    2m
dgraph-zero-0      1/1     Running   kind-worker      2m
dgraph-zero-1      1/1     Running   kind-worker2    2m
dgraph-zero-2      1/1     Running   kind-worker3    2m
```

Each of your 3 worker nodes should have exactly one Zero pod and one Alpha pod.

### Verify PVC to PV Bindings

Check that each PVC is bound to the correct PV:

```bash
kubectl get pvc
kubectl get pv
```

Each PVC should show `STATUS: Bound` and the `VOLUME` column should match a PV name.

### Verify Data Directories

Check that data directories are accessible on your host:

```bash
ls -la $HOME/dgraph-data/alpha-0/
ls -la $HOME/dgraph-data/alpha-1/
ls -la $HOME/dgraph-data/alpha-2/
```

After Dgraph starts writing data, you'll see:
- **`p/`** - Posting lists directory (contains the actual graph data)
- **`w/`** - Write-ahead log (WAL) directory

### Understanding StatefulSets

Dgraph Alpha and Zero use **StatefulSets** (not Deployments) because they require:
- **Stable pod identities**: Pods are named predictably (e.g., `dgraph-dgraph-alpha-0`, `dgraph-dgraph-alpha-1`)
- **Persistent storage**: Each pod gets its own PersistentVolumeClaim (PVC)
- **Ordered deployment**: Pods are created and terminated in a specific order

**Important StatefulSet characteristics:**
- StatefulSets do not allow most spec changes after creation (e.g., `volumeClaimTemplates`)
- Each pod gets a unique PVC based on the pod's index (e.g., `datadir-dgraph-dgraph-alpha-0`)
- Pods maintain their identity even after restarts

## Step 9: Access Dgraph

### Port Forward to Alpha Service

Access Dgraph's HTTP endpoint:

```bash
kubectl port-forward svc/dgraph-alpha-public 8080:8080
```

In another terminal, access the gRPC endpoint:

```bash
kubectl port-forward svc/dgraph-alpha-public 9080:9080
```

### Access Ratel UI (if enabled)

If Ratel is included in your Helm chart, port-forward to access the UI:

```bash
kubectl port-forward svc/dgraph-ratel 8000:8000
```

Then open [http://localhost:8000](http://localhost:8000) in your browser and enter `http://localhost:8080` as the Dgraph connection string.

### Test the Connection

Test that Dgraph is responding:

```bash
curl http://localhost:8080/health | jq
```

You should see cluster health information.

## Data Directory Mapping Reference

| Alpha Pod | Host Path (Mac) | Container Path (kind node) | PV Path | PVC Name |
|-----------|----------------|---------------------------|---------|----------|
| alpha-0 | `$HOME/dgraph-data/alpha-0` | `/dgraph-data/alpha-0` | `/dgraph-data/alpha-0` | `datadir-dgraph-dgraph-alpha-0` |
| alpha-1 | `$HOME/dgraph-data/alpha-1` | `/dgraph-data/alpha-1` | `/dgraph-data/alpha-1` | `datadir-dgraph-dgraph-alpha-1` |
| alpha-2 | `$HOME/dgraph-data/alpha-2` | `/dgraph-data/alpha-2` | `/dgraph-data/alpha-2` | `datadir-dgraph-dgraph-alpha-2` |

**Important Notes:**
- All worker nodes share the same mount point (`/dgraph-data`), but each PV uses a unique subdirectory
- Data persists even if you stop/start the kind cluster
- To completely remove data, delete the host directories: `rm -rf $HOME/dgraph-data/alpha-*`
- The `p` folders contain BadgerDB files that represent your graph data
- **Use absolute paths** for `hostPath` in PVs (shell shortcuts like `~` do not work in YAML)

## Managing the Cluster

### Stop the Cluster

To stop the cluster without deleting it (preserves data and configuration):

```bash
docker stop $(docker ps -q --filter "name=kind")
```

### Start the Cluster

To start the cluster again:

```bash
docker start $(docker ps -a -q --filter "name=kind")
```

After starting, verify nodes are ready:

```bash
kubectl get nodes
```

All nodes should show `STATUS: Ready` after a few moments.

### View Helm Release

Check your Helm release status:

```bash
helm list
```

### View Default Helm Values

To see all available configuration options:

```bash
helm show values dgraph/dgraph
```

## Clean Up

### Uninstall Dgraph

To remove Dgraph from your cluster:

```bash
helm uninstall dgraph
```

### Delete Persistent Volume Claims

Helm does not delete PVCs by default to prevent data loss. Manually delete them if needed:

```bash
kubectl delete pvc --selector="app.kubernetes.io/instance=dgraph"
```

### Delete PersistentVolumes

Delete the PVs:

```bash
kubectl delete pv dgraph-dgraph-alpha-pv-0 dgraph-dgraph-alpha-pv-1 dgraph-dgraph-alpha-pv-2
```

### Delete the kind Cluster

To completely remove the kind cluster:

```bash
kind delete cluster
```

This deletes all nodes, but your data directories on the host remain. To remove them:

```bash
rm -rf $HOME/dgraph-data/alpha-*
```

## Troubleshooting

### Pods Not Starting

If pods are stuck in `Pending` or `CrashLoopBackOff`:

**Check pod logs:**

```bash
kubectl logs dgraph-dgraph-alpha-0
```

**Check pod events:**

```bash
kubectl describe pod dgraph-dgraph-alpha-0
```

**Check node resources:**

```bash
kubectl top nodes
```

### Pods Not Distributed Across Nodes

If pods are scheduled on the same node:

**Verify anti-affinity rules:**

```bash
kubectl get pod dgraph-dgraph-alpha-0 -o yaml | grep -A 10 affinity
```

**Check node labels:**

```bash
kubectl get nodes --show-labels
```

### Debugging Storage Issues

If data isn't appearing in your host directory:

**1. Verify the PV's hostPath is correct:**

```bash
kubectl get pv dgraph-dgraph-alpha-pv-0 -o jsonpath='{.spec.hostPath.path}'
```

Ensure paths are absolute (e.g., `/Users/username/dgraph-data/alpha-0`, not `~/dgraph-data/alpha-0`).

**2. Check PVC to PV binding:**

```bash
kubectl get pvc,pv
```

PVCs should show `STATUS: Bound` and the `VOLUME` column should match a PV name.

**3. Verify pod volume mounts:**

```bash
kubectl describe pod dgraph-dgraph-alpha-0 | grep -A 10 "Mounts"
```

Confirm the mount path matches your configuration (typically `/dgraph`).

**4. Test writing to the mount path:**

```bash
kubectl exec -it dgraph-dgraph-alpha-0 -- touch /dgraph/test-file
```

Then verify the file appears in your host directory:

```bash
ls -la $HOME/dgraph-data/alpha-0/test-file
```

**5. Verify the binding chain:**

```bash
# Check which PVC the pod is using
kubectl get pod dgraph-dgraph-alpha-0 -o jsonpath='{.spec.volumes[?(@.name=="datadir")].persistentVolumeClaim.claimName}'

# Check which PV the PVC is bound to
kubectl get pvc datadir-dgraph-dgraph-alpha-0 -o jsonpath='{.spec.volumeName}'

# Check which folder the PV maps to
kubectl get pv dgraph-dgraph-alpha-pv-0 -o jsonpath='{.spec.hostPath.path}'
```

### Common Pitfalls and Solutions

#### CrashLoopBackOff

**Causes:**
- Misconfigured volumes or missing PVs
- Missing dependencies (Dgraph Alpha requires Zero to be running)
- Resource limits too low (OOM kills)
- Incorrect storage class configuration

**Solutions:**

```bash
# Check pod logs for specific errors
kubectl logs dgraph-dgraph-alpha-0

# Check resource usage
kubectl top pod dgraph-dgraph-alpha-0

# Verify Zero is running first
kubectl get pods | grep zero

# Check events
kubectl describe pod dgraph-dgraph-alpha-0
```

#### PVCs/PVs Stuck in Terminating

**Cause:** Finalizers preventing deletion or bound PVCs

**Solution - Force delete PVC:**

```bash
kubectl patch pvc <pvc-name> --type json -p '[{"op": "remove", "path": "/metadata/finalizers"}]'
```

**Solution - Force delete PV:**

```bash
kubectl patch pv <pv-name> --type json -p '[{"op": "remove", "path": "/metadata/finalizers"}]'
```

#### Silent Storage Failures

**Symptom:** PVCs remain in `Pending` state without obvious errors

**Causes:**
- Missing StorageClass
- No available PVs matching the PVC requirements
- StorageClass `volumeBindingMode` set incorrectly

**Solutions:**

```bash
# Check if StorageClass exists
kubectl get storageclass

# Check PVC status and events
kubectl describe pvc datadir-dgraph-dgraph-alpha-0

# Verify PVs are available
kubectl get pv

# Ensure StorageClass name matches in Helm values
helm get values dgraph | grep storageClass
```

#### StatefulSet Won't Update

**Cause:** StatefulSets don't allow changes to `volumeClaimTemplates` after creation

**Solution:** Delete and recreate the StatefulSet (data in PVCs will persist):

```bash
# Delete StatefulSet (pods will be recreated)
kubectl delete statefulset dgraph-dgraph-alpha

# Or use Helm upgrade with new values
helm upgrade dgraph dgraph/dgraph -f new-values.yaml
```

### Accessing Pods for Debugging

**Access pod shell:**

```bash
kubectl exec -it dgraph-dgraph-alpha-0 -- /bin/sh
```

**Check logs:**

```bash
# Current logs
kubectl logs dgraph-dgraph-alpha-0

# Follow logs
kubectl logs -f dgraph-dgraph-alpha-0

# Previous container logs (if pod restarted)
kubectl logs dgraph-dgraph-alpha-0 --previous
```

**Check volume mounts:**

```bash
kubectl describe pod dgraph-dgraph-alpha-0 | grep -A 10 "Mounts"
```

**List files in data directory:**

```bash
kubectl exec -it dgraph-dgraph-alpha-0 -- ls -la /dgraph
kubectl exec -it dgraph-dgraph-alpha-0 -- ls -la /dgraph/p
```

## Best Practices

### Storage Configuration

- **Use absolute paths** for `hostPath` volumes in PVs (e.g., `/Users/username/dgraph-data/alpha-0`, not `~/dgraph-data/alpha-0`)
- **Pre-create StorageClass and PVs** before installing the Helm chart
- **Test volume mounts** by writing a file manually to verify the mount works
- **Use `Retain` reclaim policy** on PVs to prevent accidental data loss during cleanup

### Resource Management

- **Set appropriate resource requests and limits** to avoid OOM crashes:

```yaml
alpha:
  resources:
    requests:
      cpu: "1"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "4Gi"
```

### Namespace Isolation

- **Use namespaces** to isolate releases and simplify cleanup:

```bash
kubectl create namespace dgraph
helm install dgraph dgraph/dgraph -n dgraph -f dgraph-ha-values.yaml
```

### Dependencies

- **Ensure Zero is running** before Alpha starts. Dgraph Alpha depends on Zero for cluster coordination.

## Useful Commands Reference

| Task | Command |
|------|---------|
| Check pod status | `kubectl get pods` |
| Check pod status with nodes | `kubectl get pods -o wide` |
| Access pod shell | `kubectl exec -it dgraph-dgraph-alpha-0 -- /bin/sh` |
| Check pod logs | `kubectl logs dgraph-dgraph-alpha-0` |
| Follow pod logs | `kubectl logs -f dgraph-dgraph-alpha-0` |
| Check volume mounts | `kubectl describe pod dgraph-dgraph-alpha-0 \| grep -A 10 "Mounts"` |
| Check PVC/PV binding | `kubectl get pvc,pv` |
| Check StorageClass | `kubectl get storageclass` |
| Port-forward service | `kubectl port-forward svc/dgraph-alpha-public 8080:8080` |
| Delete StatefulSet | `kubectl delete statefulset dgraph-dgraph-alpha` |
| Force delete PV | `kubectl patch pv <pv-name> --type json -p '[{"op": "remove", "path": "/metadata/finalizers"}]'` |
| Check pod events | `kubectl describe pod dgraph-dgraph-alpha-0` |
| Check node resources | `kubectl top nodes` |
| Check pod resources | `kubectl top pod dgraph-dgraph-alpha-0` |

## Next Steps

- Learn about [Dgraph configuration options](/admin/dgraph-administration)
- Explore [production deployment patterns](/installation/deployment-patterns)
- Set up [monitoring and observability](/admin/observability)
- Configure [security and access control](/admin/security)
