+++
date = "2017-03-27:12:00:00Z"
title = "Facets"
type = "docs"
weight = 60
[menu.main]
    parent = "design-concepts"
+++

Dgraph allows a set of properties to be associated with any `Relationship`. E.g. if there is a "worksFor" relationships between Node "Bob" and Node "Google", this relationship may have facet values of "since": 2002-05-05 and "position": "Engineer".

Facets can always be replaced by adding a new Node representing the relationship and storing the facet data as attriubutes of the new Node.

The term "facet" is also common in database and search engine technology, and indicates a dimension or classification of data. One way to use facets it to indicate a relationship type.
