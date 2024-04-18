from diagrams import Cluster, Diagram, Edge
from diagrams.programming.language import Go, Nodejs, Python
from diagrams.custom import Custom

graph_attr = {
    "layout":"dot",
    "compound":"true",
    "splines":"spline",
    }

zeros_attr = {
    "icon_path":"./dgraphlg.png"
}

ec2_attr = {
    "icon_path":"./dgraphlgEC2.png"
}

with Diagram("\ndgraph", show=False, direction="TB", graph_attr=graph_attr, outformat='png') as diag:
    with Cluster("RAFT Groups / Cluster (Baremetal example)"):
        with Cluster("0", graph_attr={"label":"Zero Group"}):
            a = Custom("Zero 2",  **zeros_attr)
            b = Custom("Zero 1",  **zeros_attr)
            c = Custom("Zero 0",  **zeros_attr)

        with Cluster("1", graph_attr={"label":"Alpha Group"}):
            e = Custom("Alpha 4",  **ec2_attr)
            f = Custom("Alpha 5",  **ec2_attr)
            g = Custom("Alpha 6",  **ec2_attr)
            h = Custom("Alpha 3",  **ec2_attr)
            i = Custom("Alpha 2",  **ec2_attr)
            j = Custom("Alpha 1",  **ec2_attr)
            h = Custom("Alpha 0",  **ec2_attr)

    with Cluster("2", graph_attr={"label":"APIs"}):
        e1 = Custom("RAW HTTP", "./http.png")
        f1 = Custom("gRPC", "./grpc.png") 
        g1 = Custom("GraphQL ", "./GraphQL_Logo.png")

    with Cluster("3", graph_attr={"label":"Special Node(EE)"}):
        Learner = Custom("Learner 0",  **ec2_attr)
   
    with Cluster("4", graph_attr={"label":"Clients"}):
        client2 = Custom("Apollo GraphQL ", "./apollo.png")
        client3 = Nodejs("Dgraph-JS")
        client4 = Python("Pydgraph")
        client0 = Go("Dgo")
        client1 = Custom("Curl", "./curl.png")

    b >> Edge(lhead="cluster_1") >> f

    g >> Edge(ltail="cluster_1") >> Learner
    e >> Edge(ltail="cluster_2") >> e1

    g1 >> Edge(lhead="cluster_4") >> client2
    f1 >> Edge(lhead="cluster_4") >> client0
    e1 >> Edge(lhead="cluster_4") >> client1

diag
