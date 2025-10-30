+++
title = "Unlocking Analytical Power with Dgraph"
description = "A technical guide on using Dgraph for Online Analytical Processing (OLAP) use cases, leveraging graph structure and DQL for comprehensive analytical solutions."
date = "2024-01-15T10:00:00Z"
type = "learn"
weight = 4

[menu.learn]
  parent = "learn-data-engineer"
  name = "Analytical Power with Dgraph"
  weight = 4

+++

In this guide, we explore how Dgraph, a graph database optimized for Online Transaction Processing (OLTP) and deeply nested queries, can also be used effectively for Online Analytical Processing (OLAP) use cases. We'll highlight Dgraph's analytical capabilities through examples and practical techniques for designing analytical solutions without the need for an additional OLAP solution.

## What is OLTP vs. OLAP?

**OLTP (Online Transaction Processing)** focuses on processing day-to-day transactions, while **OLAP (Online Analytical Processing)** is geared toward analyzing data from multiple sources to support business decision-making.

Dgraph, though primarily designed for OLTP, has robust features that make it capable of addressing OLAP needs by leveraging its graph structure and DQL (Dgraph Query Language).

## Relationships Form the Dimensionality

In Dgraph, relationships between nodes naturally form the dimensions required for OLAP-style analysis.

DQL's aggregation and math functions, combined with thoughtful graph design, allow you to create a comprehensive analytical solution directly within Dgraph.

The examples below use a dataset about donations to public schools in the U.S. built from public data provided by DonorsChoose.org in a [Kaggle project dataset](https://www.kaggle.com/datasets/hanselhansel/donorschoose). You can also find the data ready to load into Dgraph in the [Dgraph benchmarks GitHub repository](https://github.com/hypermodeinc/dgraph-benchmarks/tree/main/donors).

## Example: Basic Count of Projects per School

To count the number of projects per school, you can use the following DQL query:

```graphql
{
  stats(func: type(School)) {
    School.name
    count(~Project.school)
  }       
}
```

This query returns school names and the corresponding project counts:

```json
{
  "data": {
    "stats": [
      { "School.name": "Abbott Middle School", "count(~Project.school)": 16 },
      { "School.name": "Lincoln Elementary School", "count(~Project.school)": 7 },
      { "School.name": "Rosemont Early Education Center", "count(~Project.school)": 5 }
    ]
  }
}
```

## Customizing Query Results for Visualization

DQL's structure allows you to align query responses with the format needed for visualization tools. For instance, to use the query result in a Python script with Plotly, you can modify the query:

```graphql
{
  school(func: type(School)) {
    category: School.name
    value: count(~Project.school)
  }       
}
```

Using this result, you can create a bar chart in Python:

```python
import plotly.express as px
import pandas as pd

def bar_chart(payload, title='Bar Chart'):
    df = pd.json_normalize(payload['school'])
    fig = px.bar(df, y='category', x='value', title=title, orientation='h', text_auto=True)
    fig.show()

# Query result
res = {
    "school": [
        {"category": "Abbott Middle School", "value": 16},
        {"category": "Lincoln Elementary School", "value": 7},
        {"category": "Rosemont Early Education Center", "value": 5}
    ]
}

bar_chart(res, "Number of Projects per School")
```

## Advanced Aggregations and Variables

Dgraph variables add flexibility by enabling filtering, ordering, and querying additional data. Here's an example that counts projects per school and orders them by project count:

```graphql
{
  var(func: type(School)) {
    c as count(~Project.school)
  }
  serie(func: uid(c), orderdesc: val(c)) {
    category: School.name
    project_count: val(c)
  }
}
```

## Grouping and Filtering by Dimensions

Dgraph's [@groupby directive]({{< relref "/dql/query/directive/groupby.md" >}}) allows for powerful OLAP-style groupings. Here's an example of counting nodes by type:

```graphql
{
  stats(func: has(dgraph.type)) @groupby(dgraph.type) {
    count: count(uid)
  }
}
```

The response includes counts for each type, such as City, School, and Project. Additionally, you can use filtering to focus on specific dimensions.

## Complex Aggregations: Hierarchical Data

To analyze hierarchical data, such as the number and sum of donations by state and city, you can design queries that traverse node relationships:

```graphql
{
  var(func: type(State)) {
    city: ~City.state {
      ~School.city {
        School.projects {
          Project.donations {
            a as Donation.amount
          }
          s as sum(val(a))
          c as count(Project.donations)
        }
        s1 as sum(val(s))
        c1 as sum(val(c))
      }
      s2 as sum(val(s1))
      c2 as sum(val(c1))
    }
    s3 as sum(val(s2))
    c3 as sum(val(c2))
  }
  stats(func: type(State)) {
    state: State.name
    amount: val(s3)
    count: val(c3)
    city: ~City.state {
      City.name
      amount: val(s2)
      count: val(c2)
    }
  }
}
```

## Multi-Dimensional Analysis

When multiple dimensions, such as school and category, are involved but not directly related in the graph, you can split the analysis into multiple queries and combine the results in your application. Here's an example query for donations per school within a specific category:

```graphql
query stat_per_school_for_category($category: string) {
  var(func: eq(Category.name, $category)) {
    c1_projects as ~Project.category {
      c1_schools as Project.school
    }
  }
  stats(func: uid(c1_schools)) {
    School.name
    total_donation: sum(val(c1_projects))
  }
}
```

The results can then be visualized as a bubble chart in Python:

```python
import plotly.express as px
import pandas as pd

# Example data
data = [
    {"Category": "Literacy", "School": "Abbott Middle", "Total Donation": 500},
    {"Category": "Math", "School": "Lincoln Elementary", "Total Donation": 300}
]

df = pd.DataFrame(data)
fig = px.scatter(
    df, x='School', y='Category', size='Total Donation', title='Donations by School and Category'
)
fig.show()
```

## Conclusion

Dgraph's flexible graph model and powerful DQL capabilities make it a great choice for analytical use cases. By leveraging its inherent relationships, variables, and aggregation functions, you can create insightful and efficient OLAP-style analyses directly within Dgraph. Whether it's basic counts, hierarchical aggregations, or multi-dimensional data, Dgraph offers a seamless and performant solution for your analytical needs.

## Related Topics

- [DQL Query Language]({{< relref "/dql/_index.md" >}})
- [Aggregation Functions]({{< relref "/dql/query/functions.md#aggregation-functions" >}})
- [@groupby Directive]({{< relref "/dql/query/directive/groupby.md" >}})
- [Query Variables]({{< relref "/dql/query/variables.md" >}})
- [Dgraph Overview]({{< relref "/dgraph-overview.md" >}})
