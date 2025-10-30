+++
title = "Basic Jaccard Implementation"
description = "Implementing your first Jaccard distance query in DQL using variable propagation."
weight = 3

[menu.learn]
  parent = "jaccard-distance-tutorial"
  name = "Basic Implementation"
  weight = 3

+++

## Understanding Variable Propagation

Before implementing Jaccard distance, we need to understand how **variable propagation** works in DQL. This is crucial for calculating similarities across the graph.

### How Variable Propagation Works

In DQL, value variables propagate through the query tree. When you define a variable at one level, it becomes available at nested levels, and values accumulate as you traverse relationships.

{{< figure src="/images/jaccard-tutorial/variable-propagation.png" alt="Diagram showing how variables propagate through query levels" caption="Variable propagation: values accumulate as you traverse deeper into the graph" >}}

### Example: Simple Propagation

```graphql
{
  var(func: uid(0x30d72)) {  # Level 1: Start with Star Wars
    myscore as math(1)       # Assign score of 1
    genre {                  # Level 2: Follow genre edges
      ~genre {               # Level 3: Find movies with same genres
        fscore as math(myscore)  # Propagate the score
      }
    }
  }
  
  results(func: uid(fscore), orderdesc: val(fscore)) {
    name
    val(fscore)
  }
}
```

In this query:
- `myscore` starts with value 1 for Star Wars
- As we traverse `genre` edges, the variable propagates
- At level 3, `fscore` accumulates values from all paths
- Movies with more shared genres get higher scores

## Basic Jaccard Distance Query

Now let's implement Jaccard distance for finding similar movies based on genres.

### Step 1: Find Genres of Target Movie

```graphql
{
  # Get all genres for our target movie (Star Wars)
  var(func: uid(0x30d72)) {
    target_genres as genre
  }
}
```

### Step 2: Calculate Intersection and Union

```graphql
{
  # Step 1: Get target movie genres
  var(func: uid(0x30d72)) {
    target_genres as genre
  }
  
  # Step 2: For each movie, calculate intersection and union
  var(func: type(Movie)) {
    movie_genres as genre
    intersection as count(genre @filter(uid(target_genres)))
    union as math(count(genre) + count(target_genres) - val(intersection))
  }
}
```

### Step 3: Calculate Jaccard Similarity

```graphql
{
  # Get target movie genres
  var(func: uid(0x30d72)) {
    target_genres as genre
  }
  
  # Calculate similarity for all movies
  var(func: type(Movie)) {
    movie_genres as genre
    intersection as count(genre @filter(uid(target_genres)))
    union as math(count(genre) + count(target_genres) - val(intersection))
    jaccard_similarity as math(val(intersection) / val(union))
  }
  
  # Return most similar movies
  similar_movies(func: uid(jaccard_similarity), orderdesc: val(jaccard_similarity), first: 10) {
    name
    val(jaccard_similarity)
    genre {
      name
    }
  }
}
```

## Complete Working Query

Here's the complete query that finds movies similar to Star Wars:

```graphql
{
  # Get genres of target movie (Star Wars)
  var(func: uid(0x30d72)) {
    target_genres as genre
  }
  
  # Calculate Jaccard similarity for all movies
  var(func: type(Movie)) {
    movie_genres as genre
    intersection as count(genre @filter(uid(target_genres)))
    union as math(count(genre) + count(target_genres) - val(intersection))
    jaccard_similarity as math(val(intersection) / val(union))
  }
  
  # Return most similar movies
  similar_movies(func: uid(jaccard_similarity), orderdesc: val(jaccard_similarity), first: 10) {
    name
    val(jaccard_similarity)
    genre {
      name
    }
  }
}
```

## Understanding the Results

The query returns movies ranked by Jaccard similarity. Here's what the results look like:

```json
{
  "similar_movies": [
    {
      "name": "Star Wars (1977)",
      "val(jaccard_similarity)": 1.0,
      "genre": [
        {"name": "Action"},
        {"name": "Adventure"},
        {"name": "Sci-Fi"}
      ]
    },
    {
      "name": "Empire Strikes Back, The (1980)",
      "val(jaccard_similarity)": 0.75,
      "genre": [
        {"name": "Action"},
        {"name": "Adventure"},
        {"name": "Sci-Fi"}
      ]
    },
    {
      "name": "Return of the Jedi (1983)",
      "val(jaccard_similarity)": 0.75,
      "genre": [
        {"name": "Action"},
        {"name": "Adventure"},
        {"name": "Sci-Fi"}
      ]
    }
  ]
}
```

## Breaking Down the Calculation

Let's trace through the calculation for "Empire Strikes Back":

1. **Target movie genres**: `[Action, Adventure, Sci-Fi]` (3 genres)
2. **Empire Strikes Back genres**: `[Action, Adventure, Sci-Fi]` (3 genres)
3. **Intersection**: `[Action, Adventure, Sci-Fi]` (3 genres)
4. **Union**: `3 + 3 - 3 = 3` genres
5. **Jaccard Similarity**: `3/3 = 1.0`

## Common Issues and Solutions

### Issue 1: Self-Similarity
The target movie always has similarity 1.0. To exclude it:

```graphql
similar_movies(func: uid(jaccard_similarity), orderdesc: val(jaccard_similarity), first: 10) @filter(not uid(0x30d72)) {
  name
  val(jaccard_similarity)
}
```

### Issue 2: Zero Similarity Movies
Movies with no shared genres have similarity 0. To filter them out:

```graphql
similar_movies(func: uid(jaccard_similarity), orderdesc: val(jaccard_similarity), first: 10) @filter(gt(val(jaccard_similarity), 0)) {
  name
  val(jaccard_similarity)
}
```

## Performance Considerations

- **Indexing**: Ensure `genre` edges are indexed
- **Filtering**: Use `@filter` to reduce the search space
- **Limiting**: Use `first` to limit results

## Next Steps

In the next section, we'll explore advanced techniques for combining Jaccard distance with user ratings and other features.

[Continue to Advanced Techniques →]({{< relref "advanced-techniques.md" >}})
