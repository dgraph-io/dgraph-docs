+++
date = "2017-03-27T12:00:00Z"
title = "Index and Tokenizer"
type = "docs"
weight = 90
[menu.main]
    parent = "design-concepts"
+++
### Indexing
An index is an optimized data structure, stored on disk and loaded into memory, that speeds or optimizes query processing. It is created and stored in addition to the primary data. E.g. a "hasName" property or relation is the primary storage structure for a graph in Dgraph, but may also have an additional index structure configured.

Typically, Dgraph query access is optimized for forward access. When other access is needed, an index may speed up queries. Indexes are large structures that hold all values for some Relation (vs `Posting Lists`, which are typically smaller, per-Node structures).

### Tokenizers

Tokenizers are simply small algorithms that create indexed values from some Node property. E.g. if a Book Node has a Title attribute, and you add a "term" index, each word (term) in the text will be indexed. The word "Tokenizer" derives its name from tokenizing operations to create this index type.

Similary if the Book has a publicationDateTime you can add a day or year index. The "tokenizer" here extracts the value to be indexed, which may be the day or hour of the dateTime, or only the year.
