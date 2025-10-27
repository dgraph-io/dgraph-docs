+++
title = "dgraph debuginfo"
weight = 3
type = "docs"
[menu.main]
    parent = "cli"
+++

The `dgraph debuginfo` command generates comprehensive debug information about the current Dgraph node, useful for troubleshooting cluster issues.

```shell
Generate debug information on the current node
Usage:
 dgraph debuginfo [flags]

Flags:
 -a, --alpha string       Address of running dgraph alpha. (default "localhost:8080")
 -x, --archive            Whether to archive the generated report (default true)
 -d, --directory string   Directory to write the debug info into.
 -h, --help               help for debuginfo
 -p, --profiles strings   List of pprof profiles to dump in the report. (default [goroutine,heap,threadcreate,block,mutex,profile,trace])
 -s, --seconds uint32     Duration for time-based profile collection. (default 15)
 -z, --zero string        Address of running dgraph zero.

Use "dgraph debuginfo [command] --help" for more information about a command.
```