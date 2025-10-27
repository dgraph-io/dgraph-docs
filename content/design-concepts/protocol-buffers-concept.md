+++
date = "2017-03-27T12:00:00Z"
title = "Protocol Buffers"
type = "docs"
weight = 140
[menu.main]
    parent = "design-concepts"
+++

All data in Dgraph that is stored or transmitted among the Dgraph instances (servers) is converted into space-optimized byte arrays using [Protocol Buffers](https://developers.google.com/protocol-buffers/). Protocol Buffers are a standard, optimized technology to speed up network communications.
