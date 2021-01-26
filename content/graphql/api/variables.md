+++
title = "GraphQL Variables"
description = "Variables simplify GraphQL queries and mutations by letting you pass data separately."
weight = 3
[menu.main]
    parent = "api"
    name = "GraphQL Variables"
    identifier = "graphql-variables"
+++

Variables simplify GraphQL queries and mutations by letting you pass data separately. A GraphQL request can be split into two sections: one for the query or mutation, and another for variables.

Variables can be declared after the `query` or `mutation` and are passed like arguments to a function and begin with `$`.

### Query Example :

```graphql
query post($filter: PostFilter) {
	queryPost(filter: $filter) {
		title
		text
		author {
			name
		}
	}
}
```

### Variables:

```graphql
{
	"filter": {
		"title": {
			"eq": "First Post"
		}
	}
}
```

### Result:

```graphql
{
	"data": {
		"queryPost": [{
			"title": "First Post",
			"text": "Hello world!",
			"author": [{
				"name": "A.N. Author"
			}]
		}]
	}
}
```

### Mutation Example :

```graphql
mutation addAuthor($author: AddAuthorInput!) {
	addAuthor(input: [$author]) {
		author {
			name
			posts {
				title
				text
			}
		}
	}
}
```

### Variables:

```graphql
{
	"author": {
		"name": "A.N. Author",
		"dob": "2000-01-01",
		"posts": [{
			"title": "First Post",
			"text": "Hello world!"
		}]
	}
}
```

### Result:

```graphql
{
	"data": {
		"addAuthor": {
			"author": [{
				"name": "A.N. Author",
				"posts": [{
					"title": "First Post",
					"text": "Hello world!"
				}]
			}]
		}
	}
}
```