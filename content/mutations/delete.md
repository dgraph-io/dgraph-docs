+++
date = "2017-03-20T22:25:17+11:00"
title = "Delete Mutations in DQL"
description = "In this guide we explain how to use delete mutations in DQL, allowing you to delete objects of a particular type. You can also delete multiple types of data using wildcard delete."
weight = 7
[menu.main]
    name = "Delete"
    parent = "mutations"
+++

A delete mutation, identified by the `delete` keyword, removes
[triples](/mutations/triples) from the store.

For example, if the store contained the following:
```RDF
<0xf11168064b01135b> <name> "Lewis Carrol"
<0xf11168064b01135b> <died> "1998"
<0xf11168064b01135b> <dgraph.type> "Person" .
```

Then, the following delete mutation deletes the specified erroneous data, and
removes it from any indexes:

```sh
{
  delete {
     <0xf11168064b01135b> <died> "1998" .
  }
}
```

## Wildcard delete

In many cases you will need to delete multiple types of data for a predicate.
For a particular node `N`, all data for predicate `P` (and all corresponding
indexing) is removed with the pattern `S P *`.

```sh
{
  delete {
     <0xf11168064b01135b> <author.of> * .
  }
}
```

The pattern `S * *` deletes all the known edges out of a node, any reverse edges
corresponding to the removed edges, and any indexing for the removed data.

{{% notice "note" %}} For mutations that fit the `S * *` pattern, only
predicates that are among the types associated with a given node (using
`dgraph.type`) are deleted. Any predicates that don't match one of the
node's types will remain after an `S * *` delete mutation.{{% /notice %}}

```sh
{
  delete {
     <0xf11168064b01135b> * * .
  }
}
```

If the node `S` in the delete pattern `S * *` has only a few predicates with a
type defined by `dgraph.type`, then only those triples with typed predicates are
deleted. A node that contains untyped predicates will still exist after a
`S * *` delete mutation.

{{% notice "note" %}} The patterns `* P O` and `* * O` are not supported because
it's inefficient to store and find all the incoming edges. {{% /notice %}}

## Deletion of non-list predicates

Deleting the value of a non-list predicate (i.e a 1-to-1 relationship) can be
done in two ways.

* Using the [wildcard delete](#wildcard-delete) (star notation)
 mentioned in the last section.
* Setting the object to a specific value. If the value passed is not the
current value, the mutation will succeed but will have no effect. If the value
passed is the current value, the mutation will succeed and will delete the
non-list predicate.

For language-tagged values, the following special syntax is supported:

```
{
  delete {
    <0x12345> <name@es> * .
  }
}
```

In this example, the value of the `name` field that is tagged with the language
tag `es` is deleted. Other tagged values are left untouched.

## Delete Data Operation

You can delete or drop the `data` within a namespace if you are the Gaurdian of a namespace. However, you cannot delete the `schemas` or `types`. The Gaurdian of the Galaxy can trigger `drop all` and `drop data` operations across the namespaces.

For example:

```
curl 'http://localhost:8080/alter' \
  -H 'Connection: keep-alive' \
  -H 'sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"' \
  -H 'X-Dgraph-AccessToken: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MzE2MzE0MTUsImdyb3VwcyI6WyJndWFyZGlhbnMiXSwibmFtZXNwYWNlIjoxLCJ1c2VyaWQiOiJncm9vdCJ9.hMs_ySrBBl318GZ4wpeyxJgCLloAj195WxT_dVIXlas' \
  -H 'X-Auth-Token: undefined' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36' \
  -H 'Content-Type: text/plain;charset=UTF-8' \
  -H 'Accept: */*' \
  -H 'Origin: https://play.dgraph.io' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8' \
  --data-raw '{"drop_op":"DATA"}' \
  --compressed

```
