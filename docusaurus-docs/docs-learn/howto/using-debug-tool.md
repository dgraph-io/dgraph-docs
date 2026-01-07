---
title: Using the Debug Tool
---

:::note
To debug a running Dgraph cluster, first copy the postings ("p") directory to
another location. If the Dgraph cluster is not running, then you can use the
same postings directory with the debug tool.

If the “p” directory has been encrypted, then the debug tool will need to use the
--keyfile &lt;path-to-keyfile%gt; option. This file must contain the same key that was
used to encrypt the “p” directory.
:::

The `dgraph debug` tool can be used to inspect Dgraph's posting list structure.
You can use the debug tool to inspect the data, schema, and indices of your Dgraph cluster.

Some scenarios where the debug tool is useful:

- Verify that mutations committed to Dgraph have been persisted to disk.
- Verify that indices are created.
- Inspect the history of a posting list.
- Parse a badger key into meaningful struct

## Example Usage

Debug the p directory.

```sh
$ dgraph debug --postings ./p
```

Debug the p directory, not opening in read-only mode.
This is typically necessary when the database was not closed properly.

```sh
$ dgraph debug --postings ./p --readonly=false
```

Debug the p directory, only outputting the keys for the predicate `0-name`.
Note that 0 is the namespace and name is the predicate.

```sh
$ dgraph debug --postings ./p --readonly=false --pred=0-name
```

Debug the p directory, looking up a particular key:

```sh
$ dgraph debug --postings ./p --lookup 01000000000000000000046e616d65
```

Debug the p directory, inspecting the history of a particular key:

```sh
$ dgraph debug --postings ./p --lookup 01000000000000000000046e616d65 --history
```

Debug an encrypted p directory with the key in a local file at the path  ./key_file:

```sh
$ dgraph debug --postings ./p --encryption=key-file=./key_file
```


:::note
The key file contains the key used to decrypt/encrypt the db. This key should be kept secret. As a best practice,

- Do not store the key file on the disk permanently. Back it up in a safe place and delete it
  after using it with the debug tool.

- If the above is not possible, make sure correct privileges are set on the keyfile. Only the
  user who owns the dgraph process should be able to read / write the key file: `chmod 600`
:::

## Debug Tool Output

Let's go over an example with a Dgraph cluster with the following schema with a term index,
full-text index, and two separately committed mutations:

```sh
$ curl localhost:8080/alter -d '
  name: string @index(term) .
  url: string .
  description: string @index(fulltext) .
'
```

```sh
$ curl -H "Content-Type: application/rdf" "localhost:8080/mutate?commitNow=true" -d '{
  set {
    _:dgraph <name> "Dgraph" .
    _:dgraph <dgraph.type> "Software" .
    _:dgraph <url> "https://github.com/dgraph-io/dgraph" .
    _:dgraph <description> "Fast, Transactional, Distributed Graph Database." .
  }
}'
```

```sh
$ curl -H "Content-Type: application/rdf" "localhost:8080/mutate?commitNow=true" -d '{
  set {
    _:badger <name> "Badger" .
    _:badger <dgraph.type> "Software" .
    _:badger <url> "https://github.com/dgraph-io/badger" .
    _:badger <description> "Embeddable, persistent and fast key-value (KV) database written in pure Go." .
  }
}'
```

After stopping Dgraph, you can run the debug tool to inspect the postings directory:

:::note
The debug output can be very large. Typically you would redirect the debug tool to a file first for
easier analysis.
:::

```sh
$ dgraph debug --postings ./p
```

```text
Opening DB: ./p

prefix =
{d} ns: 0x0  attr: url uid: 1  ts: 5 item: [79, b0100] sz: 79 dcnt: 1 key: 000000000000000000000375726c000000000000000001
{d} ns: 0x0  attr: url uid: 2  ts: 8 item: [108, b1000] sz: 108 dcnt: 0 isz: 187 icount: 2 key: 000000000000000000000375726c000000000000000002
{d} ns: 0x0  attr: name uid: 1  ts: 5 item: [51, b0100] sz: 51 dcnt: 1 key: 00000000000000000000046e616d65000000000000000001
{d} ns: 0x0  attr: name uid: 2  ts: 8 item: [80, b1000] sz: 80 dcnt: 0 isz: 131 icount: 2 key: 00000000000000000000046e616d65000000000000000002
{i} ns: 0x0  attr: name term: [1] [badger]  ts: 8 item: [41, b1000] sz: 41 dcnt: 0 isz: 79 icount: 2 key: 00000000000000000000046e616d650201626164676572
{i} ns: 0x0  attr: name term: [1] [dgraph]  ts: 5 item: [38, b0100] sz: 38 dcnt: 1 key: 00000000000000000000046e616d650201646772617068
{d} ns: 0x0  attr: description uid: 1  ts: 5 item: [100, b0100] sz: 100 dcnt: 1 key: 000000000000000000000b6465736372697074696f6e000000000000000001
{d} ns: 0x0  attr: description uid: 2  ts: 8 item: [156, b1000] sz: 156 dcnt: 0 isz: 283 icount: 2 key: 000000000000000000000b6465736372697074696f6e000000000000000002
{i} ns: 0x0  attr: description term: [8] [databas]  ts: 8 item: [49, b1000] sz: 49 dcnt: 0 isz: 141 icount: 3 key: 000000000000000000000b6465736372697074696f6e020864617461626173
{i} ns: 0x0  attr: description term: [8] [distribut]  ts: 5 item: [48, b0100] sz: 48 dcnt: 1 key: 000000000000000000000b6465736372697074696f6e0208646973747269627574
{i} ns: 0x0  attr: description term: [8] [embedd]  ts: 8 item: [48, b1000] sz: 48 dcnt: 0 isz: 93 icount: 2 key: 000000000000000000000b6465736372697074696f6e0208656d62656464
{i} ns: 0x0  attr: description term: [8] [fast]  ts: 8 item: [46, b1000] sz: 46 dcnt: 0 isz: 132 icount: 3 key: 000000000000000000000b6465736372697074696f6e020866617374
{i} ns: 0x0  attr: description term: [8] [go]  ts: 8 item: [44, b1000] sz: 44 dcnt: 0 isz: 85 icount: 2 key: 000000000000000000000b6465736372697074696f6e0208676f
{i} ns: 0x0  attr: description term: [8] [graph]  ts: 5 item: [44, b0100] sz: 44 dcnt: 1 key: 000000000000000000000b6465736372697074696f6e02086772617068
{i} ns: 0x0  attr: description term: [8] [kei]  ts: 8 item: [45, b1000] sz: 45 dcnt: 0 isz: 87 icount: 2 key: 000000000000000000000b6465736372697074696f6e02086b6569
{i} ns: 0x0  attr: description term: [8] [kv]  ts: 8 item: [44, b1000] sz: 44 dcnt: 0 isz: 85 icount: 2 key: 000000000000000000000b6465736372697074696f6e02086b76
{i} ns: 0x0  attr: description term: [8] [persist]  ts: 8 item: [49, b1000] sz: 49 dcnt: 0 isz: 95 icount: 2 key: 000000000000000000000b6465736372697074696f6e020870657273697374
{i} ns: 0x0  attr: description term: [8] [pure]  ts: 8 item: [46, b1000] sz: 46 dcnt: 0 isz: 89 icount: 2 key: 000000000000000000000b6465736372697074696f6e020870757265
{i} ns: 0x0  attr: description term: [8] [transact]  ts: 5 item: [47, b0100] sz: 47 dcnt: 1 key: 000000000000000000000b6465736372697074696f6e02087472616e73616374
{i} ns: 0x0  attr: description term: [8] [valu]  ts: 8 item: [46, b1000] sz: 46 dcnt: 0 isz: 89 icount: 2 key: 000000000000000000000b6465736372697074696f6e020876616c75
{i} ns: 0x0  attr: description term: [8] [written]  ts: 8 item: [49, b1000] sz: 49 dcnt: 0 isz: 95 icount: 2 key: 000000000000000000000b6465736372697074696f6e02087772697474656e
{d} ns: 0x0  attr: dgraph.type uid: 1  ts: 5 item: [60, b0100] sz: 60 dcnt: 1 key: 000000000000000000000b6467726170682e74797065000000000000000001
{d} ns: 0x0  attr: dgraph.type uid: 2  ts: 8 item: [88, b1000] sz: 88 dcnt: 0 isz: 148 icount: 2 key: 000000000000000000000b6467726170682e74797065000000000000000002
{i} ns: 0x0  attr: dgraph.type term: [2] [Software]  ts: 8 item: [50, b1000] sz: 50 dcnt: 0 isz: 144 icount: 3 key: 000000000000000000000b6467726170682e747970650202536f667477617265
{s} ns: 0x0  attr: url ts: 3 item: [23, b0001] sz: 23 dcnt: 0 isz: 23 icount: 1 key: 010000000000000000000375726c
{s} ns: 0x0  attr: name ts: 3 item: [33, b0001] sz: 33 dcnt: 0 isz: 33 icount: 1 key: 01000000000000000000046e616d65
{s} ns: 0x0  attr: description ts: 3 item: [51, b0001] sz: 51 dcnt: 0 isz: 51 icount: 1 key: 010000000000000000000b6465736372697074696f6e
{s} ns: 0x0  attr: dgraph.type ts: 1 item: [50, b0001] sz: 50 dcnt: 0 isz: 50 icount: 1 key: 010000000000000000000b6467726170682e74797065
{s} ns: 0x0  attr: dgraph.drop.op ts: 1 item: [45, b0001] sz: 45 dcnt: 0 isz: 45 icount: 1 key: 010000000000000000000e6467726170682e64726f702e6f70
{s} ns: 0x0  attr: dgraph.graphql.xid ts: 1 item: [64, b0001] sz: 64 dcnt: 0 isz: 64 icount: 1 key: 01000000000000000000126467726170682e6772617068716c2e786964
{s} ns: 0x0  attr: dgraph.graphql.schema ts: 1 item: [59, b0001] sz: 59 dcnt: 0 isz: 59 icount: 1 key: 01000000000000000000156467726170682e6772617068716c2e736368656d61
{s} ns: 0x0  attr: dgraph.graphql.p_query ts: 1 item: [71, b0001] sz: 71 dcnt: 0 isz: 71 icount: 1 key: 01000000000000000000166467726170682e6772617068716c2e705f7175657279
 ns: 0x0  attr: dgraph.graphql ts: 1 item: [98, b0001] sz: 98 dcnt: 0 isz: 98 icount: 1 key: 020000000000000000000e6467726170682e6772617068716c
 ns: 0x0  attr: dgraph.graphql.persisted_query ts: 1 item: [105, b0001] sz: 105 dcnt: 0 isz: 105 icount: 1 key: 020000000000000000001e6467726170682e6772617068716c2e7065727369737465645f7175657279

Found 34 keys
```

Each line in the debug output contains a prefix indicating the type of the key: `{d}`: Data key; `{i}`: Index key;
`{c}`: Count key; `{r}`: Reverse key; `{s}`: Schema key. In the debug output above, we see data keys, index keys,
and schema keys.

Each index key has a corresponding index type. For example, in `attr: name term: [1] [dgraph]` the `[1]` shows that
this is the term index ([0x1][tok_term]); in `attr: description term: [8] [fast]`, the `[8]` shows that this is the
full-text index ([0x8][tok_fulltext]). These IDs match the index IDs in [tok.go][tok].

[tok_term]: https://github.com/dgraph-io/dgraph/blob/ce82aaafba3d9e57cf5ea1aeb9b637193441e1e2/tok/tok.go#L39
[tok_fulltext]: https://github.com/dgraph-io/dgraph/blob/ce82aaafba3d9e57cf5ea1aeb9b637193441e1e2/tok/tok.go#L48
[tok]: https://github.com/dgraph-io/dgraph/blob/ce82aaafba3d9e57cf5ea1aeb9b637193441e1e2/tok/tok.go#L37-L53

## Key Lookup

Every key can be inspected further with the `--lookup` flag for the specific key.

```sh
$ dgraph debug --postings ./p --lookup 000000000000000000000b6465736372697074696f6e020866617374
```

```text
Opening DB: ./p

Key: 000000000000000000000b6465736372697074696f6e020866617374 Length: 2 Is multi-part list? false Uid: 1 Op: 0
 Uid: 2 Op: 0
```

For data keys, a lookup shows its type and value. Below, we see that the key for `attr: url uid: 1` is a string value.

```sh
$ dgraph debug --postings ./p --lookup 000000000000000000000375726c000000000000000001
```

```text
Opening DB: ./p

Key: 000000000000000000000375726c000000000000000001 Length: 1 Is multi-part list? false Uid: 18446744073709551615 Op: 1  Type: STRING.  String Value: "https://github.com/dgraph-io/dgraph
```

For index keys, a lookup shows the UIDs that are part of this index.
Below, we see that the `fast` index for the `<description>` predicate has UIDs 0x1 and 0x2.

```sh
$ dgraph debug --postings ./p --lookup 000000000000000000000b6465736372697074696f6e020866617374
```

```text
Opening DB: ./p
Key: 000000000000000000000b6465736372697074696f6e020866617374 Length: 2 Is multi-part list? false Uid: 1 Op: 0
 Uid: 2 Op: 0
```

## Key History

You can also look up the history of values for a key using the `--history` option.

```sh
$ dgraph debug --postings ./p --lookup 000000000000000000000b6465736372697074696f6e020866617374 --history
```
```text
Opening DB: ./p

==> key: 000000000000000000000b6465736372697074696f6e020866617374. PK: UID: 0, Attr: 0-description, IsIndex: true, Term: 0
ts: 8 {item}{discard}{complete}
 Num uids = 2. Size = 16
 Uid = 1
 Uid = 2

ts: 7 {item}{delta}
 Uid: 2 Op: 1

ts: 5 {item}{delta}
 Uid: 1 Op: 1
```

Above, we see that UID 0x1 was committed to this index at ts 5, and UID 0x2 was committed to this index at ts 7.

The debug output also shows UserMeta information:

- `{complete}`: Complete posting list
- `{uid}`: UID posting list
- `{delta}`: Delta posting list
- `{empty}`: Empty posting list
- `{item}`: Item posting list
- `{deleted}`: Delete marker

## Parse Key

You can parse a key into its constituent components using `--parse_key`. This does not require a p directory.


```sh
$ dgraph debug --parse_key 000000000000000000000b6467726170682e74797065000000000000000001
```
```text
{d} Key: UID: 1, Attr: 0-dgraph.type, Data key
```
