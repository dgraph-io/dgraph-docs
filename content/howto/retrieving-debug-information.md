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

## Profiling Information with `debuginfo`

Instead of sending a request to the server for each CPU, memory, and `goroutine` profile, you can use the `debuginfo` command to collect all of these profiles, along with several metrics.

You can run the command like this:

```sh
dgraph debuginfo -a <alpha_address:port> -z <zero_address:port> -d <path_to_dir_to_store_profiles>
```

Your output should look like:

```log
I0311 14:13:53.243667   32654 run.go:118] using directory /tmp/dgraph-debuginfo037351492 for debug info dump.
I0311 14:13:53.243864   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/debug/pprof/heap
I0311 14:13:53.243872   32654 debugging.go:70] please wait... (30s)
I0311 14:13:53.245338   32654 debugging.go:58] saving heap metric in /tmp/dgraph-debuginfo037351492/alpha_heap.gz
I0311 14:13:53.245349   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/debug/pprof/profile?seconds=30
I0311 14:13:53.245357   32654 debugging.go:70] please wait... (30s)
I0311 14:14:23.250079   32654 debugging.go:58] saving cpu metric in /tmp/dgraph-debuginfo037351492/alpha_cpu.gz
I0311 14:14:23.250148   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/state
I0311 14:14:23.250173   32654 debugging.go:70] please wait... (30s)
I0311 14:14:23.255467   32654 debugging.go:58] saving state metric in /tmp/dgraph-debuginfo037351492/alpha_state.gz
I0311 14:14:23.255507   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/health
I0311 14:14:23.255528   32654 debugging.go:70] please wait... (30s)
I0311 14:14:23.257453   32654 debugging.go:58] saving health metric in /tmp/dgraph-debuginfo037351492/alpha_health.gz
I0311 14:14:23.257507   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/jemalloc
I0311 14:14:23.257548   32654 debugging.go:70] please wait... (30s)
I0311 14:14:23.259009   32654 debugging.go:58] saving jemalloc metric in /tmp/dgraph-debuginfo037351492/alpha_jemalloc.gz
I0311 14:14:23.259055   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/debug/pprof/trace?seconds=30
I0311 14:14:23.259091   32654 debugging.go:70] please wait... (30s)
I0311 14:14:53.266092   32654 debugging.go:58] saving trace metric in /tmp/dgraph-debuginfo037351492/alpha_trace.gz
I0311 14:14:53.266152   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/metrics
I0311 14:14:53.266181   32654 debugging.go:70] please wait... (30s)
I0311 14:14:53.276357   32654 debugging.go:58] saving metrics metric in /tmp/dgraph-debuginfo037351492/alpha_metrics.gz
I0311 14:14:53.276414   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/debug/vars
I0311 14:14:53.276439   32654 debugging.go:70] please wait... (30s)
I0311 14:14:53.278295   32654 debugging.go:58] saving vars metric in /tmp/dgraph-debuginfo037351492/alpha_vars.gz
I0311 14:14:53.278340   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/debug/pprof/trace?seconds=30
I0311 14:14:53.278366   32654 debugging.go:70] please wait... (30s)
I0311 14:15:23.286770   32654 debugging.go:58] saving trace metric in /tmp/dgraph-debuginfo037351492/alpha_trace.gz
I0311 14:15:23.286830   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/debug/pprof/goroutine?debug=2
I0311 14:15:23.286886   32654 debugging.go:70] please wait... (30s)
I0311 14:15:23.291120   32654 debugging.go:58] saving goroutine metric in /tmp/dgraph-debuginfo037351492/alpha_goroutine.gz
I0311 14:15:23.291164   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/debug/pprof/block
I0311 14:15:23.291192   32654 debugging.go:70] please wait... (30s)
I0311 14:15:23.304562   32654 debugging.go:58] saving block metric in /tmp/dgraph-debuginfo037351492/alpha_block.gz
I0311 14:15:23.304664   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/debug/pprof/mutex
I0311 14:15:23.304706   32654 debugging.go:70] please wait... (30s)
I0311 14:15:23.309171   32654 debugging.go:58] saving mutex metric in /tmp/dgraph-debuginfo037351492/alpha_mutex.gz
I0311 14:15:23.309228   32654 debugging.go:68] fetching information over HTTP from http://localhost:8080/debug/pprof/threadcreate
I0311 14:15:23.309256   32654 debugging.go:70] please wait... (30s)
I0311 14:15:23.313026   32654 debugging.go:58] saving threadcreate metric in /tmp/dgraph-debuginfo037351492/alpha_threadcreate.gz
I0311 14:15:23.385359   32654 run.go:150] Debuginfo archive successful: dgraph-debuginfo037351492.tar.gz
```

When the command finishes, `debuginfo` returns the tarball's file name. If no destination has been specified, the file will be created in the same directory from where you ran the `debuginfo` command. 

The following files contain the metrics collected by the `debuginfo` command:

```
dgraph-debuginfo639541060
├── alpha_block.gz
├── alpha_goroutine.gz
├── alpha_health.gz
├── alpha_heap.gz
├── alpha_jemalloc.gz
├── alpha_mutex.gz
├── alpha_profile.gz
├── alpha_state.gz
├── alpha_threadcreate.gz
├── alpha_trace.gz
├── zero_block.gz
├── zero_goroutine.gz
├── zero_health.gz
├── zero_heap.gz
├── zero_jemalloc.gz
├── zero_mutex.gz
├── zero_profile.gz
├── zero_state.gz
├── zero_threadcreate.gz
└── zero_trace.gz
```

### Command parameters

```txt
  -a, --alpha string       Address of running dgraph alpha. (default "localhost:8080")
  -x, --archive            Whether to archive the generated report (default true)
  -d, --directory string   Directory to write the debug info into.
  -h, --help               help for debuginfo
  -m, --metrics strings    List of metrics & profiles to dump in the report. (default [heap,cpu,state,health,jemalloc,trace,metrics,vars,trace,goroutine,block,mutex,threadcreate])
  -s, --seconds uint32     Duration for time-based metric collection. (default 30)
  -z, --zero string        Address of running dgraph zero.
```

#### The metrics flag (`-m`)

By default, `debuginfo` collects:
- `heap`
- `cpu`
- `state`
- `health`
- `jemalloc`
- `trace`
- `metrics`
- `vars`
- `trace`
- `goroutine`
- `block`
- `mutex`
- `threadcreate`

If needed, you can collect some of them (not necessarily all). For example, this command will collect only `jemalloc` and `health` profiles:

```sh
dgraph debuginfo -m jemalloc,health
```

### Profiles details

- `cpu profile`: CPU profile determines where a program spends its time while actively consuming CPU cycles (as opposed to while sleeping or waiting for I/O).

- `heap`: Heap profile reports memory allocation samples; used to monitor current and historical memory usage, and to check for memory leaks.

- `threadcreate`: Thread creation profile reports the sections of the program that lead the creation of new OS threads.

- `goroutine`: Goroutine profile reports the stack traces of all current goroutines.

- `block`: Block profile shows where goroutines block waiting on synchronization primitives (including timer channels). 

- `mutex`: Mutex profile reports the lock contentions. When you think your CPU is not fully utilized due to a mutex contention, use this profile. 

- `trace`: this capture a wide range of runtime events. Execution tracer is a tool to detect latency and utilization problems. You can examine how well the CPU is utilized, and when networking or syscalls are a cause of preemption for the goroutines.
Tracer is useful to identify poorly parallelized execution, understand some of the core runtime events, and how your goroutines execute.
