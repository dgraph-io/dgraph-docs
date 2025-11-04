+++
title = "MCP Server"
description = "Dgraph MCP Server"
type = "mcp"
weight = 1


[menu.mcp]
  identifier = "mcp-intro"

+++

## Model Context Protocol (MCP) Server

The [Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP)
is a standard for making tools, data, and prompts available to AI models. It can
be especially useful in bringing context on your stack into coding assistants.

Version 25 of Dgraph introduces two MCP servers with common tools for AI coding
assistants:

- `mcp` – a server that provides tools and data from your Dgraph cluster
- `mcp-ro` – a server that provides tools and data from your Dgraph cluster in
  read-only mode

### Configuration

To add the MCP server to your coding assistant, add the following to your
configuration file:

<CodeGroup>

```json local
{
  "mcpServers": {
    "dgraph": {
      "command": "npx",
      "args": ["mcp-remote", "https://localhost:9080/mcp/sse"]
    }
  }
}
```

</CodeGroup>

<Tip>
  We're continuing to refine the resources available on the MCP servers. Please
  share feedback via [Discord](https://discord.hypermode.com) or
  [GitHub](https://github.com/hypermodeinc/dgraph).
</Tip>

### Tools

The MCP servers provide the following tools:

- `Get-Schema` – fetch the schema of your cluster
- `Run-Query` – run a query on your cluster
- `Run-Mutation` – run a mutation on your cluster
- `Alter-Schema` – modify the schema of your cluster
- `Get-Common-Queries` – provides reference queries to aide in query syntax

### Prompt

For clients that support prompts over the MCP protocol, a prompt is available to
provide an introduction to the agent.

The full text of the prompt is
[available in the Dgraph repo](https://github.com/dgraph-io/dgraph/blob/8a774a03ac2558ad027bd86ead8b0059d3bfa3f5/dgraph/cmd/mcp/prompt.txt).
