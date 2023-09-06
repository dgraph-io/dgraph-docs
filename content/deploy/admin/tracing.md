+++
date = "2017-03-20T22:25:17+11:00"
title = "Tracing"
weight = 6
[menu.main]
    parent = "admin"
+++

Dgraph is integrated with [OpenCensus](https://opencensus.io/zpages/) to collect distributed traces from the Dgraph cluster.

Trace data is always collected within Dgraph. You can adjust the trace sampling rate for Dgraph queries using the `--trace` [superflag's]({{< relref "deploy/cli-command-reference.md" >}}) `ratio` option when running Dgraph Alpha nodes. By default, `--trace ratio`  is set to 0.01 to trace 1% of queries.

## Examining Traces with zPages

The most basic way to view traces is with the integrated trace pages.

OpenCensus's [zPages](https://opencensus.io/zpages/) are accessible via the Zero or Alpha HTTP port at `/z/tracez`.

## Examining Traces with Jaeger

Jaeger collects distributed traces and provides a UI to view and query traces across different services. This provides the necessary observability to figure out what is happening in the system.

Dgraph can be configured to send traces directly to a Jaeger collector with the `trace` superflag's `jaeger` option. For example, if the Jaeger collector is running on `http://localhost:14268`, then pass this option to the Dgraph Zero and Dgraph Alpha instances as `--trace jaeger=http://localhost:14268`.

See [Jaeger's Getting Started docs](https://www.jaegertracing.io/docs/getting-started/) to get up and running with Jaeger.

### Setting up multiple Dgraph clusters with Jaeger

Jaeger allows you to examine traces from multiple Dgraph clusters. To do this, use the `--collector.tags` on a Jaeger collector to set custom trace tags. For example, run one collector with `--collector.tags env=qa` and then another collector with `--collector.tags env=dev`. In Dgraph, set the `--trace jaeger` option in the Dgraph QA cluster to the first collector and set this option in the Dgraph Dev cluster to the second collector.
You can run multiple Jaeger collector components for the same single Jaeger backend (e.g., many Jaeger collectors to a single Cassandra backend). This is still a single Jaeger installation but with different collectors customizing the tags per environment.

Once you have this configured, you can filter by tags in the Jaeger UI. Filter traces by tags matching `env=dev`:

{{% load-img "/images/jaeger-ui.png" "Jaeger UI" %}}

Every trace has your custom tags set under the “Process” section of each span:

{{% load-img "/images/jaeger-server-query.png" "Jaeger Query" %}}

Filter traces by tags matching `env=qa`:

{{% load-img "/images/jaeger-json.png" "Jaeger JSON" %}}

{{% load-img "/images/jaeger-server-query-2.png" "Jaeger Query Result" %}}

### Setting up Jaeger locally
Requirements:

To set up Jaeger locally install [Docker](https://www.docker.com/) on your system.

* Example with Python and Flask:

**Step 1:** Install OpenTelemetry Packages

Install the necessary OpenTelemetry packages using pip:

```sh
pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-flask opentelemetry-exporter-jaeger
```

These packages include the OpenTelemetry API, SDK, Flask instrumentation, and Jaeger exporter.

**Step 2:** Instrument Your Flask Application

In your Flask application, import and configure OpenTelemetry. Create a Python file (e.g., app.py) and add the following code:

```python
from flask import Flask
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

app = Flask(__name__)

# Configure OpenTelemetry
resource = Resource.create({"service.name": "your-flask-app"})
trace.set_tracer_provider(TracerProvider(resource=resource))
jaeger_exporter = JaegerExporter(agent_host_name="localhost", agent_port=6831)
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument Flask
FlaskInstrumentor().instrument_app(app)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
```

This code initializes `OpenTelemetry`, configures a Jaeger exporter to send traces to a locally running Jaeger instance, and instruments your Flask application.

**Step 3:** Start a Local Jaeger Instance

Start a local Jaeger instance using Docker with the following command:

```sh
docker run -d --name jaeger \ 
-e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \ 
-p 5775:5775/udp \ 
-p 6831:6831/udp \ 
-p 6832:6832/udp \ 
-p 5778:5778 \ 
-p 16686:16686 \ 
-p 14268:14268 \ 
-p 9411:9411 \ 
jaegertracing/all-in-one:latest
```

This command starts a Docker container named `jaeger` and exposes the necessary ports for the Jaeger web interface and communication with services.

**Step 4:** Run Your Flask Application

Run your Flask application:

```sh
python app.py
```

**Step 5:** Access the Jaeger Web Interface

Visit http://localhost:16686 in your web browser to access the Jaeger web interface. You should see traces from your Flask application.


To learn more about Jaeger, see [Jaeger's Deployment Guide](https://www.jaegertracing.io/docs/deployment/).
