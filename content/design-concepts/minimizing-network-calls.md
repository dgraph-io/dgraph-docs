+++
date = "2017-03-20T22:25:17+11:00"
title = "How Dgraph Minimizes Network Calls"
weight = 4
[menu.main]
    parent = "design-concepts"
+++

# Predicate-based storage and sharding

Dgraph is unique in its use of predicate-based sharding, which allows complex and deep distributed queries to run without incurring high network overhead and associated delays. 

Rather than store and shard by putting different _nodes_ (aka entities<sup>*</sup>) on different servers, Dgraph stores predicates or triples of the form <node1> <predicateRelation> <node2>. The nodes are therefore implicit in the predicate storage, rather than vice versa.

This makes querying much different and particularly allows network optimizations in a distributed database.

# Example
To explain how this works, let's use an example query:

  `Find all posts liked by friends of friends of mine over the last year, written by a popular author A.`

## SQL/NoSQL
In a distributed SQL database or (non-graph) NoSQL database, this query requires retrieval of a lot of data. Consider two approaches:

Approach 1:

* Find all the friends (~ 338 [friends](https://www.pewresearch.org/fact-tank/2014/02/03/what-people-like-dislike-about-facebook/)).
* Find all their friends (~ 338 * 338 = 40,000 people).
* Find all the posts liked by these people over the last year (resulting set in the millions).
* Intersect these posts with posts authored by person A.

Approach 2:

* Find all posts written by popular author A over the last year (possibly thousands).
* Find all people who liked those posts (easily millions) (call this `result set 1`).
* Find all your friends.
* Find all their friends (call this `result set 2`).
* Intersect `result set 1` with `result set 2`.

Both approaches wouild result in a lot of data moving back and forth between database and
application; would be slow to execute, and may require running an offline job.

## Dgraph Approach
This is how it would run in Dgraph:

Sharding assumptions (which predicates live where):
* Assume Server X contains the predicate `friends` representing all friend relations. 
* Assume Server Y contains the predicate `posts_liked` representing who likes each post. 
* Assume Server Z contains the predicate `author` representing all who authored each post. 
* Assume Server W contains the predicate `title` representing the uid->string title property of posts. 

Algorithm:
* Server X
    * If the request was not sent to Server X, route it to Server X where the friends predicate lives. **(1 RPC)**.
    * Seek to my uid within predicate (tablet) `friends` and retrieve a list of my friends as a list of uids.
    * Still on Server X, use the friends predicate again to get friends for all of those uids, generating a list of my friends of friends. Call this `result set myFOF`.
* Server Y
    * Send result set myFOF to Server Y, which holds the posts_liked predicate **(1 RPC)**.
    * Retrieve all posts liked by my friends-of-friends. Call this `result set postsMyFOFLiked`.
* Server Z
    * Send postsMyFOFLiked result set to Server Z **(1 RPC)**. 
    * Retrieve all posts authored by A. Call this `result set authoredByA`.
    * Still on Server Z, intersect the two sorted lists to get posts that are both liked and authored by A: `result set postsMyFOFLiked` intersect `result set authoredByA`. Call this `result set postsMyFOFLikedByA`
   * at this point we have done the hard work, but have the uids of the posts, instead of the post titles.
* Server W
    * Send `result set postsMyFOFLikedByA` to Server W which holds the title predicate **(1 RPC)**.
    * Convert uids to names by looking up the title for each uid. `result set postUidsAndTitles`
* Respond to caller with `result set postUidsAndTitles`.

## Net Result - predictable distributed graph scaling
In at most 4 RPCs, we have figured out all the posts liked by friends of friends, written by popular author X, with titles. Typically, all four predicates will not live on four different Servers, so this is a worst-case scenario. Dgraph network activity is limited to the level of query join depth, rather than increasing arbitrarily according to the number of nodes in the graph, and how they are broken up across servers.

There is no way we are aware of that a node-based sharding database can avoid high network RPC counts during arbitrary queries because "node-hopping" does not mix well with a graph that is segmented across servers.


----
<sup>*</sup> _Throughout this note, we call entities in a graph "nodes" which is a standard terminology when talking about nodes and predicates. Elsewhere we call nodes "entities" to avoid confusion with K8s "nodes."_