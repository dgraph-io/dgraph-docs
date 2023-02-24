+++
title = "Monitoring with Prometheus"
weight = 8
[menu.main]
    name = "Monitoring with Prometheus"
    parent = "cloud-admin"
+++

Dgraph Cloud provides enterprises with real-time observability and high-fidelity telemetry of their instances with [Prometheus](https://prometheus.io/). Once enabled Dgraph exposes real-time values for **Dedicated** backends at any given instant via the `/prometheus` endpoint. You can also configure Grafana for real-time visualization and analysis thus allowing for in-depth visibility into the behavior, performance and health of your instances.

{{% notice "note" %}}
Prometheus integration is only available to users of **Dedicated Instance** types and not **Free** or **Shared Instance**.
{{% /notice %}}

### Enable Prometheus for your instance

To enable Prometheus with your Dgraph Cloud instance: 

1. Login to Dgraph Cloud Dashboard, select **Settings** under the **Admin** subsection and then select **Modify Backend**. Alternately, you can also enable Prometheus while launching a new backend.

2. For your existing **Dgraph Cloud Backend**, enable the **Prometheus** option under **Additional Settings**. Review and select one of the available configurations viz. 1C (1 vCPU 4GB RAM), 2C, 4C, or 8C.

3. Review the estimated hourly cost which should include additional charges for enabling Prometheus. Click **Launch** to submit changes.

![Enable Prometheus](/images/monitoring/enable_prometheus.png)

### Configure your instance endpoint with Prometheus

1. For all dedicated backends with Prometheus enabled, a new endpoint called `/prometheus` would be available. For example, a backend at URL https://sudomain.region.cloud-provider.cloud.dgraph.io/graphql would expose metrics at URL - https://sudomain.region.cloud-provider.cloud.dgraph.io/prometheus

2. The `/prometheus` endpoint is protected with the **Admin API key**. Upon accessing the URL for this endpoint, you will be prompted to enter the key. More information on creating an Admin API key can be found [here](https://dgraph.io/docs/cloud/admin/authentication/).

   ![Enter Admin API key](/images/monitoring/api_token.png)

3. Once you enter the Admin API token click **Submit** to launch the **Prometheus Dashboard**.

   ![Prometheus Dashboard](/images/monitoring/prometheus_dashboard.png)

### Integrating with Grafana

To visualize Prometheus metrics within the **Grafana Dashboard** for Dgraph Cloud, perform the following actions:

1. Launch the Grafana Dashboard and follow the same steps to add a **Prometheus Datasource** to Grafana as described **[here](https://prometheus.io/docs/visualization/grafana/#creating-a-prometheus-data-source)** but with the following changes:

2. Under the section **HTTP**, for the option **URL**, enter the URL for your Prometheus endpoint (Example - https://sudomain.region.cloud-provider.cloud.dgraph.io/prometheus). For the **Access** option select **Server (default)** from the dropdown menu.

3. Lastly, under **Auth**, within the **Custom HTTP Headers** subsection, click **Add Header** and add a new **Header** called `X-Auth-Token`. Enter your Admin API key as its **Value**. The following image shows an example data source configuration.

   ![Grafana Config](/images/monitoring/grafana_config.png)

4. Click **Save & Test** to save and test the new Prometheus data source.

5. Create and populate your **Grafana Dashboard**. Select the **Prometheus Data Source** that was configured earlier and select the metrics to visualize (e.g. dgraph_memory_inuse_bytes, dgraph_alpha_health_status etc). 
   If correctly configured the metrics can be visualized as below:
   
   ![Grafana Config](/images/monitoring/grafana_dashboard.png)

Your new monitoring and observability stack for Dgraph Cloud leveraging the Prometheus and Grafana solutions should now be ready for use. The same is useful to monitor your Dgraph backend efficiently, without the overhead of installing, maintaining, and scaling your own observability stack.

