+++
title = "Advanced Techniques"
description = "Combining Jaccard distance with ratings, implementing weighted similarity, and optimizing queries for production."
weight = 4

[menu.learn]
  parent = "jaccard-distance-tutorial"
  name = "Advanced Techniques"
  weight = 4

+++

## Combining Jaccard Distance with Ratings

Pure Jaccard distance only considers genre overlap. To create better recommendations, we can combine it with user ratings and other factors.

### Weighted Jaccard Similarity

We can enhance the basic Jaccard similarity by incorporating average ratings:

{{< math >}}
$$d(M_1, M_2) = |M_1.genres \cap M_2.genres| + M_2.\overline{rating}$$
{{< /math >}}

Where:
- `|M_1.genres ∩ M_2.genres|` is the number of shared genres
- `M_2.rating` is the average rating of movie M₂

### Implementation with Ratings

```graphql
{
  # Get target movie genres
  var(func: uid(0x30d72)) {
    target_genres as genre
  }
  
  # Calculate average rating for every movie
  var(func: type(Movie)) {
    allmovies as rated @facets(a as rating) {
      c as count(~rated)
      avg_rating as math(a / c)
    }
  }
  
  # Calculate weighted similarity
  var(func: uid(allmovies)) {
    intersection as count(genre @filter(uid(target_genres)))
    avg_rating as math(avg_rating)
    weighted_score as math(val(intersection) + val(avg_rating))
  }
  
  # Return top recommendations
  recommendations(func: uid(weighted_score), orderdesc: val(weighted_score), first: 10) {
    name
    val(weighted_score)
    genre {
      name
    }
  }
}
```

## Cosine Distance Implementation

For more sophisticated similarity, we can implement cosine distance, which considers both genre overlap and rating similarity.

### Mathematical Foundation

Cosine distance treats movies as vectors where:
- Dimensions represent genres (1 if present, 0 if not)
- Last dimension represents average rating

{{< math >}}
$$\text{cosine\_similarity} = \frac{\vec{M_1} \cdot \vec{M_2}}{|\vec{M_1}| \times |\vec{M_2}|}$$
{{< /math >}}

### DQL Implementation

```graphql
{
  # Calculate average rating for every movie
  var(func: type(Movie)) {
    rated @facets(r as rating) {
      c as count(~rated)
      M2_avg_rating as math(r / c)
      M2_num_gen as count(genre)
    }
  }
  
  # Calculate cosine similarity
  var(func: uid(0x30d72)) {
    # Target movie properties
    M1_num_ratings as count(~rated)
    ~rated @facets(B as rating)
    M1_ratings_sum as sum(val(B))
    M1_avg_rating as math(M1_ratings_sum / M1_num_ratings)
    M1_num_gen as count(genre)
    
    # Find movies with shared genres
    genre {
      ~genre {
        # Calculate cosine similarity
        genint as count(genre @filter(uid(M1_genres)))
        score as math((genint + (M1_avg_rating * M2_avg_rating)) /
          (sqrt(M1_num_gen + (M1_avg_rating * M1_avg_rating)) *
           sqrt(M2_num_gen + (M2_avg_rating * M2_avg_rating))))
      }
    }
  }
  
  # Return similar movies
  similar_movies(func: uid(score), orderdesc: val(score), first: 10) {
    name
    val(score)
  }
}
```

## Next Steps

In the final section, we'll conclude this tutorial and discuss next steps for implementing recommendations in your own applications.

[Continue to Real-World Applications →]({{< relref "applications.md" >}})
