+++
title = "Lambda Server"
description = "Setup a Dgraph database with a lambda server. Dgraph Lambda is a serverless platform for running JavaScript on Dgraph and Dgraph Cloud."
weight = 6
[menu.main]
    parent = "lambda"
+++

In this article you'll learn how to setup a Dgraph database with a lambda server.

## Dgraph Lambda

[Dgraph Lambda](https://github.com/dgraph-io/dgraph-lambda) is a serverless platform for running JavaScript on Dgraph and [Dgraph Cloud](https://dgraph.io/cloud).

You can [download the latest version](https://github.com/dgraph-io/dgraph-lambda/releases/latest) or review the implementation in our [open-source repository](https://github.com/dgraph-io/dgraph-lambda).

### Running with Docker

To run a Dgraph Lambda server with Docker:
```bash
docker run -it --rm -p 8686:8686 -v /path/to/script.js:/app/script/script.js -e DGRAPH_URL=http://host.docker.internal:8080 dgraph/dgraph-lambda
```

{{% notice "note" %}}
`host.docker.internal` doesn't work on older versions of Docker on Linux. You can use `DGRAPH_URL=http://172.17.0.1:8080` instead.
{{% /notice %}}


### Adding libraries

If you would like to add libraries to Dgraph Lambda, use `webpack --target=webworker` to compile your script.

### Working with TypeScript

You can import `@slash-graphql/lambda-types` to get types for `addGraphQLResolver` and `addGraphQLMultiParentResolver`.


## Dgraph Alpha

To set up Dgraph Alpha, you need to define the `--graphql` superflag's `lambda-url` option, which is used to set the URL of the lambda server. All the `@lambda` fields will be resolved through the lambda functions implemented on the given lambda server.

For example:

```bash
dgraph alpha --graphql lambda-url=http://localhost:8686/graphql-worker
```

Then test it out with the following `curl` command:
```bash
curl localhost:8686/graphql-worker -H "Content-Type: application/json" -d '{"resolver":"MyType.customField","parent":[{"customField":"Dgraph Labs"}]}'
```

### Docker settings

If you're using Docker, you need to add the `--graphql` superflag's `lambda-url` option to your Alpha configuration. For example:

```yml
    command: /gobin/dgraph alpha --zero=zero1:5180 -o 100 --expose_trace --trace ratio=1.0
      --profile_mode block --block_rate 10 --logtostderr -v=2
      --security whitelist=10.0.0.0/8,172.16.0.0/12,192.168.0.0/16 --my=alpha1:7180
      --graphql lambda-url=http://lambda:8686/graphql-worker
```

Next, you need to add the Dgraph Lambda server configuration, and map the JavaScript file that contains the code for lambda functions to the `/app/script/script.js` file. Remember to set the `DGRAPH_URL` environment variable to your Alpha server.


Here's a complete Docker example that uses the base Dgraph image and adds Lambda server support:

```yml
services:
  dgraph:
    image: dgraph/standalone:latest
    environment: 
      DGRAPH_ALPHA_GRAPHQL: "lambda-url=http://dgraph_lambda:8686/graphql-worker"
    ports:
      - "8080:8080"
      - "9080:9080"
      - "8000:8000"
    volumes:
      - dgraph:/dgraph

  dgraph_lambda:
    image: dgraph/dgraph-lambda:latest

    ports:
      - "8686:8686"
    environment:
      DGRAPH_URL: http://dgraph:8080
    volumes:
      - ./gql/script.js:/app/script/script.js:ro

volumes:
  dgraph: {}
```
