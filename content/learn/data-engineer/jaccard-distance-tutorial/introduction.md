+++
title = "Introduction to Jaccard Distance"
description = "Understanding the mathematical foundation of Jaccard distance and its role in content-based filtering for recommendation systems."
weight = 1

[menu.learn]
  parent = "jaccard-distance-tutorial"
  name = "Introduction"
  weight = 1

+++

## What is Jaccard Distance?

**Jaccard distance** is a measure of dissimilarity between two sets. It's widely used in recommendation systems, information retrieval, and data mining to find similar items based on their properties.

The Jaccard distance between two sets A and B is defined as:

{{< math >}}
$$d_J(A, B) = 1 - \frac{|A \cap B|}{|A \cup B|}$$
{{< /math >}}

Where:
- `|A ∩ B|` is the size of the intersection of sets A and B
- `|A ∪ B|` is the size of the union of sets A and B

## Jaccard Similarity vs Distance

The **Jaccard similarity** is the complement of the distance:

{{< math >}}
$$J(A, B) = \frac{|A \cap B|}{|A \cup B|} = 1 - d_J(A, B)$$
{{< /math >}}

- **Similarity**: Higher values (closer to 1) indicate more similar items
- **Distance**: Lower values (closer to 0) indicate more similar items

## Why Jaccard Distance for Recommendations?

### 1. **Set-Based Similarity**
Jaccard distance works perfectly with categorical data like:
- Movie genres
- Product categories
- User interests
- Tags and labels

### 2. **Handles Sparse Data**
Unlike other similarity measures, Jaccard distance:
- Works well with sparse datasets
- Doesn't require numerical ratings
- Focuses on presence/absence of features

### 3. **Interpretable Results**
- Values range from 0 to 1
- Easy to understand and interpret
- Can be used as confidence scores

## Example: Movie Genres

Consider two movies with the following genres:

**Movie A**: `[Action, Adventure, Sci-Fi]`
**Movie B**: `[Action, Adventure, Drama]`

Let's calculate their Jaccard similarity:

- **Intersection**: `[Action, Adventure]` → Size = 2
- **Union**: `[Action, Adventure, Sci-Fi, Drama]` → Size = 4
- **Jaccard Similarity**: `2/4 = 0.5`
- **Jaccard Distance**: `1 - 0.5 = 0.5`

## Content-Based Filtering

Content-based filtering recommends items based on their properties rather than user behavior. The process:

1. **Extract Features**: Identify relevant properties (genres, actors, directors)
2. **Calculate Similarity**: Use Jaccard distance to find similar items
3. **Rank Results**: Sort by similarity score
4. **Recommend**: Suggest the most similar items

## Advantages of Content-Based Filtering

- **No Cold Start Problem**: Works for new users and items
- **Transparent**: Easy to explain why items are recommended
- **Domain Knowledge**: Can incorporate expert knowledge about items
- **Diverse Recommendations**: Less likely to create filter bubbles

## Next Steps

In the next section, we'll set up the Movielens dataset in Dgraph and explore how to structure the data for Jaccard distance calculations.

[Continue to Dataset Setup →]({{< relref "dataset-setup.md" >}})
