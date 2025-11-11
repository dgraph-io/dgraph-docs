import React, { ReactNode } from 'react';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';

interface ClientExampleProps {
  children: ReactNode;
}

// Helper function to extract code from MDX children
function extractCodeFromChildren(children: ReactNode): string {
  if (typeof children === 'string') {
    return children.trim();
  }

  let code = '';
  
  React.Children.forEach(children, (child) => {
    if (typeof child === 'string') {
      code += child;
    } else if (React.isValidElement(child)) {
      const props = child.props as { children?: ReactNode; className?: string };
      // Check if it's a code element or has code in props
      if (props?.children) {
        code += extractCodeFromChildren(props.children);
      } else if (props?.className && props.className.includes('language-')) {
        // It's a code element with language class
        if (props.children) {
          code += extractCodeFromChildren(props.children);
        }
      }
    }
  });
  
  return code.trim();
}

export default function ClientExample({ children }: ClientExampleProps) {
  // Extract code content from children
  const codeContent = extractCodeFromChildren(children);
  
  // Escape backticks and dollar signs for template literals
  const escapeForTemplate = (str: string) => {
    return str.replace(/`/g, '\\`').replace(/\$/g, '\\$');
  };
  
  const escapedCode = escapeForTemplate(codeContent);

  return (
    <Tabs>
      <TabItem value="go-grpc" label="Go">
        <CodeBlock language="go">
{`package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"

    "google.golang.org/grpc"
    "github.com/dgraph-io/dgo/v230"
    "github.com/dgraph-io/dgo/v230/protos/api"
)

func main() {
    conn, err := grpc.Dial("localhost:9080", grpc.WithInsecure())
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    dgraphClient := dgo.NewDgraphClient(api.NewDgraphClient(conn))
    ctx := context.Background()

    txn := dgraphClient.NewTxn()
    defer txn.Discard(ctx)

    query := \`${escapedCode}\`
    
    resp, err := txn.Query(ctx, query)
    if err != nil {
        log.Fatal(err)
    }

    var result map[string]interface{}
    json.Unmarshal(resp.Json, &result)
    fmt.Printf("%+v\\n", result)
}`}
        </CodeBlock>
      </TabItem>
      <TabItem value="java" label="Java">
        <CodeBlock language="java">
{`import io.dgraph.DgraphClient;
import io.dgraph.DgraphGrpc;
import io.dgraph.DgraphProto;
import io.dgraph.Transaction;

import java.util.Map;

public class App {
    public static void main(String[] args) {
        ManagedChannel channel = ManagedChannelBuilder
            .forAddress("localhost", 9080)
            .usePlaintext()
            .build();
        
        DgraphGrpc.DgraphStub stub = DgraphGrpc.newStub(channel);
        DgraphClient dgraphClient = new DgraphClient(stub);
        
        String query = "${escapedCode.replace(/"/g, '\\"')}";
        
        Transaction txn = dgraphClient.newTransaction();
        try {
            DgraphProto.Response response = txn.query(query);
            System.out.println(response.getJson().toStringUtf8());
        } finally {
            txn.discard();
        }
    }
}`}
        </CodeBlock>
      </TabItem>
      <TabItem value="python" label="Python">
        <CodeBlock language="python">
{`import grpc
from dgraph import DgraphClient, Txn

def main():
    client_stub = DgraphClient("localhost:9080")
    client = DgraphClient(client_stub)
    
    query = """${escapedCode}"""
    
    txn = client.txn()
    try:
        response = txn.query(query)
        print(response.json)
    finally:
        txn.discard()

if __name__ == "__main__":
    main()`}
        </CodeBlock>
      </TabItem>
      <TabItem value="js-grpc" label="JavaScript (gRPC)">
        <CodeBlock language="javascript">
{`const dgraph = require("dgraph-js");
const grpc = require("grpc");

async function main() {
    const clientStub = new dgraph.DgraphClientStub(
        "localhost:9080",
        grpc.credentials.createInsecure()
    );
    const dgraphClient = new dgraph.DgraphClient(clientStub);
    
    const query = \`${escapedCode}\`;
    
    const txn = dgraphClient.newTxn();
    try {
        const res = await txn.query(query);
        const json = res.getJson();
        console.log(JSON.stringify(JSON.parse(json), null, 2));
    } finally {
        await txn.discard();
    }
}

main().catch((e) => {
    console.error(e);
});`}
        </CodeBlock>
      </TabItem>
      <TabItem value="js-http" label="JavaScript (HTTP)">
        <CodeBlock language="javascript">
{`const fetch = require("node-fetch");

async function main() {
    const query = \`${escapedCode}\`;
    
    const response = await fetch("http://localhost:8080/query", {
        method: "POST",
        headers: {
            "Content-Type": "application/dql"
        },
        body: query
    });
    
    const result = await response.json();
    console.log(JSON.stringify(result, null, 2));
}

main().catch((e) => {
    console.error(e);
});`}
        </CodeBlock>
      </TabItem>
      <TabItem value="curl" label="Curl">
        <CodeBlock language="bash">
{`curl -X POST http://localhost:8080/query \\
  -H "Content-Type: application/dql" \\
  -d '${codeContent.replace(/'/g, "'\\''")}'`}
        </CodeBlock>
      </TabItem>
    </Tabs>
  );
}

