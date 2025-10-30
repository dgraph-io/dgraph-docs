+++
title = "Setting Up the Dataset"
description = "Preparing the Movielens ML-100k dataset for Jaccard distance calculations in Dgraph."
weight = 2

[menu.learn]
  parent = "jaccard-distance-tutorial"
  name = "Dataset Setup"
  weight = 2

+++

## Movielens ML-100k Dataset

The [Movielens ML-100k dataset](https://grouplens.org/datasets/movielens/) is a classic dataset for recommendation systems research. It contains:

- **100,000 ratings** from 1,000 users on 1,700 movies
- **User demographics**: age, gender, occupation, zip code
- **Movie metadata**: title, release date, genres
- **Rating scale**: 1-5 stars

## Graph Schema Design

To implement Jaccard distance in Dgraph, we need to structure the data as a graph where:

- **Movies** are nodes with genre properties
- **Users** are nodes with rating relationships to movies
- **Genres** are separate nodes connected to movies

### Schema Definition

```graphql
type Movie {
  name: string
  release_date: datetime
  genre: [Genre]
  rated: [User] @reverse
}

type User {
  name: string
  age: int
  gender: string
  occupation: string
  rated: [Movie] @reverse
}

type Genre {
  name: string
  ~genre: [Movie]
}
```

### Rating Facets

Ratings are stored as facets on the `rated` relationship:

```graphql
# User rates a movie with a 5-star rating
<user_id> <rated> <movie_id> (rating: 5) .
```

## Sample Data Structure

Here's how the data looks in RDF format:

```turtle
# Movie nodes
<0x30d72> <dgraph.type> "Movie" .
<0x30d72> <name> "Star Wars (1977)" .
<0x30d72> <release_date> "1977-05-25" .

# Genre nodes
<0x1> <dgraph.type> "Genre" .
<0x1> <name> "Action" .
<0x2> <dgraph.type> "Genre" .
<0x2> <name> "Adventure" .
<0x3> <dgraph.type> "Genre" .
<0x3> <name> "Sci-Fi" .

# Genre relationships
<0x30d72> <genre> <0x1> .
<0x30d72> <genre> <0x2> .
<0x30d72> <genre> <0x3> .

# User rating
<0x1001> <dgraph.type> "User" .
<0x1001> <name> "Alice" .
<0x1001> <rated> <0x30d72> (rating: 5) .
```

## Loading the Dataset

The dataset was converted to RDF format (the dataset and script can be found at [GitHub](https://github.com)) and loaded into Dgraph. The conversion process transforms the CSV data into graph relationships where:

- Movies are nodes connected to genre nodes
- Users are nodes with `rated` relationships to movies
- Ratings are stored as facets on the `rated` edge

## Understanding the Graph Structure

The resulting graph structure looks like this:

{{< figure src="/images/jaccard-tutorial/graph-structure.png" alt="Graph structure showing movies, genres, and users" caption="Graph structure with movies connected to genres and users connected to movies via ratings" >}}

### Key Relationships

- **Movie → Genre**: Many-to-many relationship
- **User → Movie**: One-to-many with rating facet
- **Genre ← Movie**: Reverse relationship for efficient queries

## Querying the Schema

Let's verify our data is loaded correctly:

```graphql
{
  # Count total movies
  movieCount(func: type(Movie)) {
    count(uid)
  }
  
  # Count total genres
  genreCount(func: type(Genre)) {
    count(uid)
  }
  
  # Sample movie with genres
  sampleMovie(func: type(Movie), first: 1) {
    name
    genre {
      name
    }
  }
}
```

## Expected Results

After loading, you should see:
- ~1,700 movies
- ~19 unique genres
- ~100,000 rating relationships
- Proper genre connections

## Next Steps

Now that we have our dataset loaded, we can implement Jaccard distance calculations. In the next section, we'll build our first similarity query.

[Continue to Basic Implementation →]({{< relref "basic-implementation.md" >}})
