+++
title = "Troubleshooting"
weight = 20
[menu.main]
    parent = "deploy"
+++

This page provides tips on how to troubleshoot issues with running Dgraph.

### Running out of memory (OOM)

When you [bulk load]({{< relref "deploy/fast-data-loading/bulk-loader.md" >}})
or [backup]({{< relref "/enterprise-features/binary-backups.md" >}}) your data,
Dgraph can consume more memory than usual due to a high volume of writes. This
can cause OOM crashes.

You can take the following steps to help avoid OOM crashes:

* **Increase the amount of memory available**: If you run Dgraph with insufficient
memory, that can result in OOM crashes. The recommended minimum RAM to run Dgraph
on desktops and laptops (single-host deployment) is 16GB. For servers in a 
cluster deployment, the recommended minimum is 8GB per server. This applies to
EC2 and GCE instances, as well as on-premises servers.
* **Reduce the number of Go routines**: You can troubleshoot OOM issues by reducing
the number of Go routines (`goroutines`) used by Dgraph from the default value
of eight. For example, you can reduce the `goroutines` that Dgraph uses to four
by calling the `dgraph alpha` command with the following option: 

  `--badger "goroutines=4"`


### Too many open files

If you see an log error messages saying `too many open files`, you should increase the per-process file descriptors limit.

During normal operations, Dgraph must be able to open many files. Your operating system may set by default a open file descriptor limit lower than what's needed for a database such as Dgraph.

On Linux and Mac, you can check the file descriptor limit with `ulimit -n -H` for the hard limit and `ulimit -n -S` for the soft limit. The soft limit should be set high enough for Dgraph to run properly. A soft limit of 65535 is a good lower bound for a production setup. You can adjust the limit as needed.
