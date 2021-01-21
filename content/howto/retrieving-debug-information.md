+++
date = "2017-03-20T22:25:17+11:00"
title = "Retrieving Debug Information"
weight = 1
[menu.main]
    parent = "howto"
+++

Each Dgraph data node exposes profile over `/debug/pprof` endpoint and metrics over `/debug/vars` endpoint. Each Dgraph data node has it's own profiling and metrics information. Below is a list of debugging information exposed by Dgraph and the corresponding commands to retrieve them.

## Metrics Information

If you are collecting these metrics from outside the Dgraph instance you need to pass `--expose_trace=true` flag, otherwise there metrics can be collected by connecting to the instance over localhost.

```
curl http://<IP>:<HTTP_PORT>/debug/vars
```

Metrics can also be retrieved in the Prometheus format at `/debug/prometheus_metrics`. See the [Metrics]({{< relref "deploy/metrics.md" >}}) section for the full list of metrics.

## Profiling Information

Profiling information is available via the `go tool pprof` profiling tool built into Go. The ["Profiling Go programs"](https://blog.golang.org/profiling-go-programs) Go blog post will help you get started with using pprof. Each Dgraph Zero and Dgraph Alpha exposes a debug endpoint at `/debug/pprof/<profile>` via the HTTP port.

```
go tool pprof http://<IP>:<HTTP_PORT>/debug/pprof/heap
Fetching profile from ...
Saved Profile in ...
```
The output of the command would show the location where the profile is stored.

In the interactive pprof shell, you can use commands like `top` to get a listing of the top functions in the profile, `web` to get a visual graph of the profile opened in a web browser, or `list` to display a code listing with profiling information overlaid.

### CPU Profile

```
go tool pprof http://<IP>:<HTTP_PORT>/debug/pprof/profile
```

### Memory Profile

```
go tool pprof http://<IP>:<HTTP_PORT>/debug/pprof/heap
```

### Block Profile

Dgraph by default doesn't collect the block profile. Dgraph must be started with `--profile_mode=block` and `--block_rate=<N>` with N > 1.

```
go tool pprof http://<IP>:<HTTP_PORT>/debug/pprof/block
```

### Goroutine stack

The HTTP page `/debug/pprof/` is available at the HTTP port of a Dgraph Zero or Dgraph Alpha. From this page a link to the "full goroutine stack dump" is available (e.g., on a Dgraph Alpha this page would be at `http://localhost:8080/debug/pprof/goroutine?debug=2`). Looking at the full goroutine stack can be useful to understand goroutine usage at that moment.

## debuginfo

Context

Sometimes (very frequently) users report issues with memory and CPU consumptions while using Dgraph. Apart from asking what they are doing, type of workload, logs we also ask for profiles. To get these profiles the user has to send a request to the server and this has to be done for CPU and Memory profiles. We also have goroutine profiles that need to be requested via curl, wget or go. We have documentation on how to get them here but sometimes it gets frustrating to send several requests when we ask them.

To simplify this process, we have a command called `debuginfo` that collects all the profiles we need

### How does it work

You can run the command like this:

```sh
dgraph debuginfo -a <alpha_address:port> -z <zero_address:port> -d <path_to_dir_to_store_profiles> 
```

It comes with the following flags:

```
  -a, --alpha string       Address of running dgraph alpha. (default "localhost:8080")
  -x, --archive            Whether to archive the generated report (default true)
  -d, --directory string   Directory to write the debug info into.
  -h, --help               help for debuginfo
  -p, --profiles strings   List of pprof profiles to dump in the report. (default [goroutine,heap,threadcreate,block,mutex,profile,trace])
  -s, --seconds uint32     Duration for time-based profile collection. (default 15)
  -z, --zero string        Address of running dgraph zero.
```

The flags are self-explanatory, btw I’d like to spend a couple of words on the following flags:

The “-p” flag (profile flag)

 By default, it collects `goroutine`, `heap`, `threadcreate`, `block`, `mutex`, `profile`, `trace` - Anyway if needed you can collect some of them (not necessarily all) with a similar command:

```sh
dgraph debuginfo -p goroutine,heap
```

This command will collect only goroutine and heap profiles

The “-s” flag (seconds flag)

By default is set to 15seconds and that should be fine for all the profiles that we are collecting except for the cpu profile, this profile needs at least 30sec to be collected therefore when we want to collect it (most of the times) we need to tune the -s flag as follows:

```sh
dgraph debug info -s 30
```

I’m working on fixing that to set it to a default value of 30sec so we dont need to specify this flag. Anyway for the time being that flag is required if we want to collect a cpu profile. 

If we miss that flag we will get a context deadline exceeded:

```log
I0120 14:06:49.840613   13589 pprof.go:72] fetching profile over HTTP from http://localhost:8080/debug/pprof/profile?duration=15
I0120 14:06:49.840622   13589 pprof.go:74] please wait... (15s)
E0120 14:07:14.341613   13589 pprof.go:58] error while saving pprof profile from http://localhost:8080/debug/pprof/profile?duration=15: http fetch: Get "http://localhost:8080/debug/pprof/profile?duration=15": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
```

What is the output you will get when running that command:

Your output will look like:

```log
[Decoder]: Using assembly version of decoder
Page Size: 4096
I0120 14:57:43.722166   15018 run.go:85] using directory /tmp/dgraph-debuginfo121781350 for debug info dump.
I0120 14:57:43.722272   15018 pprof.go:72] fetching profile over HTTP from http://localhost:8080/debug/pprof/goroutine?duration=30
I0120 14:57:43.722281   15018 pprof.go:74] please wait... (30s)
I0120 14:57:43.724208   15018 pprof.go:62] saving goroutine profile in /tmp/dgraph-debuginfo121781350/alpha_goroutine.gz
I0120 14:57:43.724217   15018 pprof.go:72] fetching profile over HTTP from http://localhost:8080/debug/pprof/heap?duration=30
I0120 14:57:43.724222   15018 pprof.go:74] please wait... (30s)
I0120 14:57:43.726212   15018 pprof.go:62] saving heap profile in /tmp/dgraph-debuginfo121781350/alpha_heap.gz
I0120 14:57:43.726220   15018 pprof.go:72] fetching profile over HTTP from http://localhost:8080/debug/pprof/threadcreate?duration=30
I0120 14:57:43.726225   15018 pprof.go:74] please wait... (30s)
I0120 14:57:43.727054   15018 pprof.go:62] saving threadcreate profile in /tmp/dgraph-debuginfo121781350/alpha_threadcreate.gz
I0120 14:57:43.727064   15018 pprof.go:72] fetching profile over HTTP from http://localhost:8080/debug/pprof/block?duration=30
I0120 14:57:43.727071   15018 pprof.go:74] please wait... (30s)
I0120 14:57:43.727958   15018 pprof.go:62] saving block profile in /tmp/dgraph-debuginfo121781350/alpha_block.gz
I0120 14:57:43.727967   15018 pprof.go:72] fetching profile over HTTP from http://localhost:8080/debug/pprof/mutex?duration=30
I0120 14:57:43.727971   15018 pprof.go:74] please wait... (30s)
I0120 14:57:43.728622   15018 pprof.go:62] saving mutex profile in /tmp/dgraph-debuginfo121781350/alpha_mutex.gz
I0120 14:57:43.728630   15018 pprof.go:72] fetching profile over HTTP from http://localhost:8080/debug/pprof/profile?duration=30
I0120 14:57:43.728635   15018 pprof.go:74] please wait... (30s)
I0120 14:58:13.788794   15018 pprof.go:62] saving profile profile in /tmp/dgraph-debuginfo121781350/alpha_profile.gz
I0120 14:58:13.788827   15018 pprof.go:72] fetching profile over HTTP from http://localhost:8080/debug/pprof/trace?duration=30
I0120 14:58:13.788841   15018 pprof.go:74] please wait... (30s)
I0120 14:58:14.792110   15018 pprof.go:62] saving trace profile in /tmp/dgraph-debuginfo121781350/alpha_trace.gz
I0120 14:58:14.799585   15018 run.go:115] Debuginfo archive successful: dgraph-debuginfo121781350.tar.gz
```

as you can see at the end it will say where this tarball dir has been saved. In my case it has been saved in `/tmp/dgraph-debuginfo121781350/alpha_trace.gz` because I did not specify the -d flag to give a custom path

### What does each profile mean

- `cpu profile`: CPU profile determines where a program spends its time while actively consuming CPU cycles (as opposed to while sleeping or waiting for I/O).

- `heap`: Heap profile reports memory allocation samples; used to monitor current and historical memory usage, and to check for memory leaks.

- `threadcreate`: Thread creation profile reports the sections of the program that lead the creation of new OS threads.

- `goroutine`: Goroutine profile reports the stack traces of all current goroutines.

- `block`: Block profile shows where goroutines block waiting on synchronization primitives (including timer channels). 

- `mutex`: Mutex profile reports the lock contentions. When you think your CPU is not fully utilized due to a mutex contention, use this profile. 

- `trace`:  this capture a wide range of runtime events.  Execution tracer is a tool to detect latency and utilization problems. You can examine how well the CPU is utilized, and when networking or syscalls are a cause of preemption for the goroutines.

Tracer is useful to:

Understand how your goroutines execute.

Understand some of the core runtime events such as GC runs.

Identify poorly parallelized execution.

