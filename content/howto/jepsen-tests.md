+++
date = "2017-03-20T22:25:17+11:00"
title = "Run Jepsen Tests"
weight = 10
[menu.main]
    parent = "howto"
+++

1. Clone the Jepsen repo at [https://github.com/jepsen-io/jepsen](https://github.com/jepsen-io/jepsen).

```sh
git clone git@github.com:jepsen-io/jepsen.git
```

2. Run the following command to setup the instances from the repo.

```sh
cd docker && ./up.sh
```

This should start 5 Jepsen nodes in docker containers.

3. Now ssh into `jepsen-control` container and run the tests.

```sh
docker exec -it jepsen-control bash
```

```sh
root@control:/jepsen# cd dgraph
root@control:/jepsen/dgraph# lein run test -w upsert

# Specify a --package-url

root@control:/jepsen/dgraph# lein run test --force-download --package-url https://github.com/dgraph-io/dgraph/releases/download/nightly/dgraph-linux-amd64.tar.gz -w upsert
```