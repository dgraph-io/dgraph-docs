+++
title = "Graphs and Natural Data Modeling"
description ="Graphs provide an alternative to tabular data structures, allowing for a more natural way to store and retrieve data."
type = "learn"
weight = 1
[menu.learn]
  name = "Data Model"
  parent = "dm-101"
  identifier = "dm-101-intro"
+++

Graphs provide an alternative to tabular data structures, allowing for a
more natural way to store and retrieve data.

For example, you could imagine that we are modeling a conversation within a
family:

* A `father`, who starts a conversation about going to get ice cream.
* A `mother`, who comments that she would also like ice cream.
* A `child`, who likes the idea of the family going to get ice cream.

This conversation could easily occur in the context of a modern social media or
messaging app, so you can imagine the data model for such an app as follows:

![A graph diagram for a social media app's data model](/images/data-model/evolution-3.png)

For the remainder of this module, we will use this as our example application:
a basic social media or messaging app, with a data model that includes
`people`, `posts`, `comments`, and `reactions`.

A graph data model is different from a relational model. A graph focuses on the
relationships between information, whereas a relational model focuses on
storing similar information in a list. The graph model received its name because
it resembles a graph when illustrated.

* Data objects are called *nodes* and are illustrated with a circle.
* Properties of nodes are called *predicates* and are illustrated as a panel
  on the node.
* Relationships between nodes are called *edges* and are illustrated as
  connecting lines. Edges are named to describe the relationship between two
  nodes. A `reaction` is an example of an edge, in which a person reacts to a
  post.

Some illustrations omit the predicates panel and show only the nodes and edges.

Referring back to the example app, the `father`, `mother`, `child`, `post`, and `comment`
are nodes. The name of the people, the post's title, and text of the comment
are the predicates. The natural relationships between the authors of the posts,
authors of the comments, and the comments' topics are edges.

As you can see, a graph models data in a natural way that shows the
relationships (edges) between the entities (nodes) that contain predicates.
