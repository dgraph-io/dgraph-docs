---
title: "Dgraph Experimental"
description: "Explore experimental tools, scripts, and projects for Dgraph development, testing, and data import."
---

The [dgraph-experimental](https://github.com/dgraph-io/dgraph-experimental) repository contains a collection of tools, scripts, and experimental projects that complement Dgraph. These resources are community-contributed and maintained—use them as starting points and adapt them to your needs.

:::warning Experimental Code
These tools are **not officially supported**. Review, understand, and test them before using in production environments.
:::

## Data Import Tools

### CSV to RDF Converter

Convert CSV files to RDF format for Dgraph import using template-based mapping.

- **Template-based mapping**: Define how CSV columns map to RDF triples
- **Functions**: Built-in support for geolocation, datetime conversion, and random dates
- **Flexible**: Handle any CSV structure without requiring specific node/edge formats

📁 [data-import/csv-to-rdf](https://github.com/dgraph-io/dgraph-experimental/tree/main/data-import/csv-to-rdf)

### Dgraph Import (v25.0+)

The unified `dgraph import` command simplifies bulk loading by combining schema deployment and data streaming into a single operation.

📁 [dgraph-import](https://github.com/dgraph-io/dgraph-experimental/tree/main/dgraph-import)

## Docker Images

### FOAF Graph Demo

A self-contained Docker image with a pre-populated Friend-of-a-Friend graph and Jupyter notebooks demonstrating DQL and GraphQL queries.

📁 [docker/foaf_graph](https://github.com/dgraph-io/dgraph-experimental/tree/main/docker/foaf_graph)

### Standalone Bulk Loader

A Docker image for learning Dgraph that automatically bulk loads data from an `import` folder on startup.

- Place RDF files in the `import` directory
- Optionally include `.schema` (DQL) and `.graphql` schema files
- The container handles bulk loading automatically

📁 [docker/standalone_bulk_loader](https://github.com/dgraph-io/dgraph-experimental/tree/main/docker/standalone_bulk_loader)

## Testing & Analysis

### Locust Load Testing

A complete load testing framework for Dgraph using [Locust](https://locust.io/).

- Test queries, mutations, or mixed workloads
- Web UI for real-time monitoring
- Configurable concurrency and duration
- Automatic Go profiling integration

📁 [dgraph-locust](https://github.com/dgraph-io/dgraph-experimental/tree/main/dgraph-locust)

### Analysis Tools

Scripts for analyzing Dgraph operations and performance:

- **processProfiles**: Convert Go profiles (CPU, heap, goroutines) to SVG visualizations
- **DQLParse**: Scan and deduplicate queries from Dgraph request logs
- **compactionAnalysis**: Parse and analyze BadgerDB compaction activity

📁 [analysisTools](https://github.com/dgraph-io/dgraph-experimental/tree/main/analysisTools)

## AI & Development Tools

### Cursor Rules for DQL

Pre-built [Cursor AI](https://cursor.sh/) rules that help generate valid DQL queries. These rules teach the AI assistant DQL syntax, patterns, and best practices.

📁 [dql-helper/cursor-rules](https://github.com/dgraph-io/dgraph-experimental/tree/main/dql-helper/cursor-rules)

### Ecommerce Agent

An AI agent for product discovery and recommendations using:
- Dgraph Knowledge Graph
- Google Gen AI Toolbox
- LangChain + Gemini Pro

📁 [ecommerce-agent-dgraph-toolbox](https://github.com/dgraph-io/dgraph-experimental/tree/main/ecommerce-agent-dgraph-toolbox)

## Knowledge Graph

### Generic Knowledge Graph

Experimental project exploring generic (non-domain-specific) knowledge graphs with:
- Entity extraction from unstructured text
- Ontology-based schema design
- Modus API integration

📁 [knowledge-graph/generic-kg](https://github.com/dgraph-io/dgraph-experimental/tree/main/knowledge-graph/generic-kg)

### KGkit (Work in Progress)

Python package for building knowledge graphs from tabular and unstructured data:
- Automatic entity detection from CSV column naming conventions
- Geolocation handling
- PDF and text extraction

📁 [knowledge-graph/KGkit](https://github.com/dgraph-io/dgraph-experimental/tree/main/knowledge-graph/KGkit)

## Contributing

Found a bug or have an improvement? Contributions are welcome:

1. Fork the [dgraph-experimental repository](https://github.com/dgraph-io/dgraph-experimental)
2. Create a feature branch
3. Submit a pull request

For questions or discussions, visit the [Dgraph Community](https://discuss.dgraph.io/).

