+++
date = "2017-03-20T22:25:17+11:00"
title = "CSV data"
weight = 6
[menu.main]
    parent = "migration"
+++

## Convert CSV to JSON

There are many tools available to convert CSV to JSON. You can import large data sets to Dgraph using [Dgraph Live Loader]({{< relref "/deploy/fast-data-loading/live-loader.md" >}}) or [Dgraph Bulk Loader]({{< relref "/deploy/fast-data-loading/bulk-loader.md" >}}). In these examples, the `csv2json` tool is used, and the data is imported using the **Mutate** tab in Ratel.

### Before you begin

* Install [`csv2json`](https://www.npmjs.com/package/csv2json) conversion tool.
* Install `jq` a lightweight and flexible command-line JSON processor.
* Connect the Dgraph instance to Ratel for queries, mutations and visualizations.

#### Example 1

1. Create a `names.csv` file with these details:

    ```csv
    Name,URL
    Dgraph,https://github.com/dgraph-io/dgraph
    Badger,https://github.com/dgraph-io/badger
    ```

2. Change to the directory that conntains the `names.csv` file and convert it to `names.json`:

    ```sh
    $ csv2json names.csv --out names.json
    ```
3. To prettify a JSON file, use the jq '.' command:

    ```sh
    $ cat names.json | jq '.'
    ```
    The output is similar to:
    ```sh
    [
      {
        "Name": "Dgraph",
        "URL": "https://github.com/dgraph-io/dgraph"
      },
      {
        "Name": "Badger",
        "URL": "https://github.com/dgraph-io/badger"
      }
    ]
    ```

    This JSON file follows
    the [JSON Mutation Format]({{< relref "mutations/json-mutation-format.md" >}}), it can be loaded into Dgraph using [Dgraph Live Loader]({{< relref "/deploy/fast-data-loading/live-loader.md" >}}) , [Dgraph Bulk Loader]({{< relref "/deploy/fast-data-loading/bulk-loader.md" >}}) or the programmatic clients.

4. To load the data to Ratel and HTTP clients. The JSON data has to be stored within the `"set"`
[key]({{< relref "mutations/json-mutation-format.md#json-syntax-using-raw-http-or-ratel-ui"
>}}). You can use `jq` to transform the JSON into the correct format:

    ```sh
    $ cat names.json | jq '{ set: . }'
    ```

    An output simialr to this appears:
    ```json
    {
      "set": [
        {
          "Name": "Dgraph",
          "URL": "https://github.com/dgraph-io/dgraph"
        },
        {
          "Name": "Badger",
          "URL": "https://github.com/dgraph-io/badger"
        }
      ]
    }
    ```
5. Paste the output in the **Mutate** tab of **Console** in Ratel.
6. Click **Run** to import data.
7. To view the imported data paste the following in the **Query** tab and click **Run**:

    ```dql
    {
     names(func: has(URL)) {
     Name
     }
    }
    ```


#### Example 2

1. Create a `connects.csv` file that's connecting nodes together. The `connects` field should be of the `uid` type.

    ```csv
    uid,connects
    _:a,_:b
    _:a,_:c
    _:c,_:d
    _:d,_:a
    ```

2. To get the correct JSON format, you can convert the CSV into JSON and use `jq`
to transform it in the correct format where the `connects` edge is a node `uid`. 
This JSON file can be loaded into Dgraph using the programmatic clients. 

    ```sh
    $ csv2json connects.csv | jq '[ .[] | { uid: .uid, connects: { uid: .connects } } ]'
    ```
    The output is similar to:
    
    ```json
    [
      {
        "uid": "_:a",
        "connects": {
          "uid": "_:b"
        }
      },
      {
        "uid": "_:a",
        "connects": {
          "uid": "_:c"
        }
      },
      {
        "uid": "_:c",
        "connects": {
          "uid": "_:d"
        }
      },
      {
        "uid": "_:d",
        "connects": {
          "uid": "_:a"
        }
      }
    ]
    ```

3. To get an output of the mutation format accepted in Ratel UI and HTTP clients:

    ```sh
    $ csv2json connects.csv | jq '{ set: [ .[] | {uid: .uid, connects: { uid: .connects } } ] }'
    ```

    The output is similar to:

    ```json
    {
      "set": [
        {
          "uid": "_:a",
          "connects": {
            "uid": "_:b"
          }
        },
        {
          "uid": "_:a",
          "connects": {
            "uid": "_:c"
          }
        },
        {
          "uid": "_:c",
          "connects": {
            "uid": "_:d"
          }
        },
        {
          "uid": "_:d",
          "connects": {
            "uid": "_:a"
          }
        }
      ]
    }
    ```
{{% notice "note" %}}
To reuse existing integer IDs from a CSV file as UIDs in Dgraph, use Dgraph Zero's [assign endpoint]({{< relref "deploy/dgraph-zero" >}}) before loading data to allocate a range of UIDs that can be safely assigned.
{{% /notice %}}

4. Paste the output in the **Mutate** tab of **Console** in Ratel, and click **Run** to import data.