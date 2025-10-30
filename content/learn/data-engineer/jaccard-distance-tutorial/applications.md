+++
title = "Real-World Applications"
description = "Conclusion and next steps for implementing Jaccard distance recommendations in practice."
weight = 5

[menu.learn]
  parent = "jaccard-distance-tutorial"
  name = "Real-World Applications"
  weight = 5

+++

## Summary

In this tutorial, we've demonstrated how to implement Jaccard distance for content-based filtering in Dgraph using DQL queries. We've covered:

1. **Basic Jaccard Distance**: Finding similar movies based on genre overlap
2. **Weighted Similarity**: Combining genre overlap with average ratings
3. **Cosine Distance**: A more sophisticated similarity measure that considers both genre intersection and rating similarity

These techniques leverage Dgraph's variable propagation feature to calculate similarity scores directly within the graph database, making it efficient to find similar items based on their properties.

## Key Takeaways

### Variable Propagation

The key to implementing similarity calculations in Dgraph is understanding how value variables propagate through query blocks. As you traverse relationships in the graph, variables accumulate values from all paths, allowing you to:

- Sum values across multiple relationships
- Normalize scores by path counts
- Calculate intersections and unions for set-based similarity

### Content-Based Filtering

Content-based filtering recommendations work by:

1. **Extracting properties**: Identify relevant features (genres, categories, attributes)
2. **Calculating similarity**: Use distance functions like Jaccard or Cosine
3. **Ranking results**: Sort items by similarity score
4. **Recommending**: Return the most similar items

This approach doesn't suffer from the "cold start" problem—you can recommend items even if they have no ratings, as long as they have properties to compare.

## Query Optimization Tips

When implementing similarity queries in production:

- **Use filters early**: Filter by type or existence of properties before calculating similarity
- **Limit intermediate results**: Use `first` to limit the number of items processed
- **Filter zero similarity**: Exclude items with no overlap using `@filter(gt(val(similarity), 0))`
- **Index predicates**: Ensure genre edges are properly indexed for efficient traversal

## Next Steps: Collaborative Filtering

This tutorial focused on **content-based filtering**, which recommends items based on their properties. The next step is to explore **collaborative filtering**, which recommends items based on user behavior and similarity between users.

Collaborative filtering can be implemented in Dgraph by:

- Finding users with similar rating patterns
- Using variable propagation to aggregate preferences
- Combining user similarity with item similarity for hybrid recommendations

## Machine Learning Integration

While this tutorial showed how to implement similarity calculations directly in DQL queries, you can also:

- Run machine learning algorithms over Dgraph data
- Use Dgraph queries to extract features for ML models
- Combine graph-based recommendations with ML-based recommendations
- Use Dgraph's graph structure as input to graph neural networks

## Further Exploration

The techniques shown here can be applied to various domains:

- **E-commerce**: Recommend products based on category overlap
- **Content platforms**: Find similar articles, videos, or posts based on tags
- **Music services**: Recommend songs based on genre and metadata
- **Social networks**: Find similar users based on interests and connections

The key is to identify the relevant properties in your domain and structure them as graph relationships in Dgraph, then use DQL's variable propagation to calculate similarity.

## Further Reading

- [DQL Query Language]({{< relref "/dql/_index.md" >}})
- [DQL Functions]({{< relref "/dql/query/functions.md" >}})
- [Query Variables]({{< relref "/dql/query/variables.md" >}})
- [@groupby Directive]({{< relref "/dql/query/directive/groupby.md" >}}) - Useful for aggregating similarity scores
- [Stanford Mining Massive Datasets](http://www.mmds.org/) - Textbook on recommendation systems theory