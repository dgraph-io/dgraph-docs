---
title: "Graph Data Models 101"
description: "Learn data modeling using relational databases compared to graph databases such as Dgraph,"
---

When building an app, you might wonder which database is the best choice. A
traditional relational database that you can query using SQL is a familiar
choice, but does a relational database really provide a natural fit to your data
model, and the performance that you need if your app goes viral and needs to scale
up rapidly? 

This tutorial takes a deeper look at data modeling using relational
databases compared to graph databases like Dgraph, to give you a better
understanding of the advantages of using a graph database to power your app. If
you aren't familiar with graph data models or graph databases, this tutorial was
written for you.

### Learning Goals
In this tutorial, you will learn about graphs, and how a graph
database is different from a database built on a relational data model. You
will not find any code or syntax in this tutorial, but rather a comparison of
graphs and relational data models. By the end of this tutorial, you will be
able to answer the following questions:

* What is a graph?
* How are graphs different from relational models?
* How is data modeled in a graph?
* How is data queried from a graph?

Along the way, you might find that a graph is the right fit for the data model
used by your app. Any data model that tracks lots of different relationships (or
*edges*) between various data types is a good candidate for a graph model.

Whether this is the first time you are learning about graphs or 
looking to deepen your understanding of graphs with some concrete examples, this
tutorial will help you along your journey.
