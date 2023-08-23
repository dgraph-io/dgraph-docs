+++
title = "GraphQL Queries"
type = "learn"
tutorial = "courses/messageboardapp/react"
pageType = "tutorial"
description = "In this step, you can move on to the GraphQL queries that get the data to render the main pages, thanks to Apollo Client, Dgraph Cloud, and React routing."
weight = 16
[menu.learn]
  name = "GraphQL Queries"
  parent = "react-app-ui"
  identifier = "react-app-ui-queries"
[nav]
  nextpage = "react-ui-graphql-mutations.md"
[nav.previous]
title = "React Routing"
link = "/courses/messageboardapp/react/develop/react/react-routing/"
[nav.next]
title = "GraphQL Mutations"
link = "/courses/messageboardapp/react/develop/react/graphql-mutations/"
+++

With Apollo Client set up and connected to your Dgraph Cloud backend, and React
routing set up, you can move on to the GraphQL queries that get the data to
render the main pages.

You'll use [GraphQL Code Generator](https://graphql-code-generator.com/) to generate typed React hooks that help contact the GraphQL endpoint, and then use those hooks in the React components to get the data.

## GraphQL Code Generator

The Apollo Client libraries give you generic React hooks to contact GraphQL backends, but [GraphQL Code Generator](https://graphql-code-generator.com/) takes that to the next level by using GraphQL introspection to generate types with hooks specific to the API you are using.  That means all your GraphQL calls are typed and if anything ever changes, you'll know at development time.

Firstly, add all the GraphQL Code Generator dependencies as development dependencies to the project with:

```sh
yarn add -D @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-operations @graphql-codegen/typescript-react-apollo @graphql-codegen/add @graphql-codegen/near-operation-file-preset @graphql-codegen/named-operations-object
```

You can then run the following command to to set up GraphQL Code Generator for
the project:

```sh
yarn graphql-codegen init
> ... answer questions ...
```

However, you can skip the setup steps and jump straight to using it by adding a
file, `codegen.yml`, in the top-level project directory. The following is the
configuration needed for this project. Remember to replace
`<<Dgraph Cloud-GraphQL-URL>>` with the URL or your Dgraph Cloud endpoint.


```yaml
overwrite: true
schema: "<<Dgraph Cloud-GraphQL-URL>>"
documents:
  - 'src/**/*.graphql'
generates:
  src/types/graphql.ts:
    plugins:
      - typescript
  src/:
    preset: near-operation-file
    presetConfig:
      baseTypesPath: types/graphql
      folder: types
      extension: .ts
    plugins:
      - typescript-operations
      - typescript-react-apollo
      - named-operations-object
    config:
      reactApolloVersion: 3
      withHOC: false
      withHooks: true
      withComponent: false
```

That configuration tells GraphQL Code Generator to introspect the schema of your GraphQL API, generate using the `typescript` plugin and place the generated code `near-operation-file` (we'll see what that means just below).

Then, add `"generate-types": "graphql-codegen --config codegen.yml"` to the scripts key in package.json, so it now looks like:

```json
"scripts": {
  "start": "react-scripts start",
  "build": "react-scripts build",
  "test": "react-scripts test",
  "eject": "react-scripts eject",
  "generate-types": "graphql-codegen --config codegen.yml"
}
```

Now, whenever the schema of your GraphQL database changes, you can regenerate the project's types with:

```sh
yarn run generate-types
```

Running that now, won't do anything though, because you have to start your GraphQL development first.

## GraphQL operations

You can layout the source of a Dgraph Cloud project however you wish. For this tutorial you'll use the following project structure.

```
public
scripts
src
  components
    component1.tsx
    component2.tsx
    operations.graphql
    types
      operations.ts
  ...
  types
    graphql.ts
```

You'll write GraphQL queries and mutations in the `operations.graphql` file.  Then, run GraphQL Code Generator and it generates the `src/types/graphql.ts` file with global types for the things that make sense globally and `src/components/types/operations.ts` for things that are local to the components.

Having `operations.graphql` file in the directory for the components that it applies to makes it really easy to find the GraphQL (rather than it being split as strings in a number of javascript files) while still making it clear what components the GraphQL applies to.  If your project gets larger, you might end up with more project structure and more operations files, but the general process still works.

Start by creating the `scr/components/operations.graphql` file and add a query to find the data for home page's list of posts.

```graphql
query allPosts {
  queryPost(order: { desc: datePublished }) {
    id
    title
    tags
    datePublished
    category {
      id
      name
    }
    author {
      username
      displayName
      avatarImg
    }
    commentsAggregate {
      count
    }
  }
}
```

Then run:

```sh
yarn run generate-types
```

...and GraphQL Code Generator will create the `src/types/graphql.ts` and `src/components/types/operations.ts` files.  If your interested in what was generated, open up those files and you'll see how much the code generator did.  If you want to use that to build a UI, read on.

## GraphQL React hooks

Of the things that GraphQL Code Generator built after introspecting your GraphQL endpoint, it's the React hooks you'll use most in building a UI.

From the `allPosts` query in the `operations.graphql` file, GraphQL Code Generator built a hook `useAllPostsQuery` with everything you need to make that GraphQL query.

In general, you'll use it like this

```js
const { data, loading, error } = useAllPostsQuery()

if (loading) { /* render loading indicator */ }

if (error) { /* handle error */ }

// layout using 'data'
```

The `data` result will have exactly the same structure as the `allPosts` operation, and it's typed, so you can layout with confidence by for example using `map` on the post list returned by `queryPost` and then indexing into each post.

```
data?.queryPost?.map((post) => {
  ...
  post?.author.username
  ...
}
```

Because of the types, you really can't go wrong.

## Layout with GraphQL - post list

Now that you have GraphQL to help write queries and get data and GraphQL Code Generator to turn that into typed Javascript, you can now layout your data and be sure you won't make a mistake because GraphQL and types will catch you.

Let's make a `PostFeed` component that uses the `useAllPostsQuery` and renders the data into a Semantic React UI `Table`.

```js
import React from "react"
import {
  Header,
  Label,
  Loader,
  Image,
  Table,
  Container,
} from "semantic-ui-react"
import { useAllPostsQuery } from "./types/operations"
import { Link } from "react-router-dom"
import { avatar } from "./avatar"

export function PostFeed() {
  const { data, loading, error } = useAllPostsQuery()
  if (loading) return <Loader active />
  if (error) {
    return (
      <Container text className="mt-24">
        <Header as="h1">Ouch! That page didn't load</Header>
        <p>Here's why : {error.message}</p>
      </Container>
    )
  }

  const items = data?.queryPost?.map((post) => {
    const likes = Math.floor(Math.random() * 10)
    const replies = post?.commentsAggregate?.count
    const tagsArray = post?.tags?.trim().split(/\s+/) || []

    return (
      <Table.Row key={post?.id}>
        <Table.Cell>
          <Link
            to={{
              pathname: "/post/" + post?.id,
            }}
          >
            <Header as="h4" image>
              <Image src={avatar(post?.author.avatarImg)} rounded size="mini" />
              <Header.Content>
                {post?.title}
                <Header.Subheader>{post?.author.username}</Header.Subheader>
              </Header.Content>
            </Header>
          </Link>
        </Table.Cell>
        <Table.Cell>
          <span className="ui red empty mini circular label"></span>{" "}
          {" " + post?.category.name}
        </Table.Cell>
        <Table.Cell>
          {tagsArray.map((tag) => {
            if (tag !== "") {
              return (
                <Label as="a" basic color="grey" key={tag}>
                  {tag}
                </Label>
              )
            }
            return " "
          })}
        </Table.Cell>
        <Table.Cell>
          <p>
            <i className="heart outline icon"></i> {likes} Like
            {likes === 1 ? "" : "s"}
          </p>
          <p>
            {" "}
            <i className="comment outline icon"></i> {replies}{" "}
            {replies === 1 ? "Reply" : "Replies"}
          </p>
        </Table.Cell>
      </Table.Row>
    )
  })

  return (
    <>
      <Table basic="very">
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>Posts</Table.HeaderCell>
            <Table.HeaderCell>Category</Table.HeaderCell>
            <Table.HeaderCell>Tags</Table.HeaderCell>
            <Table.HeaderCell>Responses</Table.HeaderCell>
          </Table.Row>
        </Table.Header>

        <Table.Body>{items}</Table.Body>
      </Table>
    </>
  )
}
```

There's some layout and CSS styling in there, but the actual data layout is just indexing into the queried data with `post?.title`, `post?.author.username`, etc.
Note that the title of the post is made into a link with the following:

```js
<Link to={{pathname: "/post/" + post?.id}}> ... </Link>
```

When clicked, this link will go through the React router to render the post
component.

You can add whatever avatar links you like into the data, and you'll do that
later in the tutorial after you add authorization and logins; but for now, make
a file `src/components/avatar.ts` and fill it with this function that uses
random avatars we've supplied with the app boilerplate, as follows:

```js
export function avatar(img: string | null | undefined) {
  return img ?? "/" + Math.floor(Math.random() * (9 - 1) + 1) + ".svg"
}
```

Then, update the `src/components/home.tsx` component to render the post list, as
follows:

```js
import React from "react"
import { PostFeed } from "./posts"

export function Home() {
  return <div className="layout-margin">{PostFeed()}</div>
}
```

With this much in place, you will see a home screen (start the app with `yarn start` if you haven't already) with a post list of the sample data you have added to your Dgraph Cloud database.

![post list component](/images/message-board/post-list-component.png)

Each post title in the post list is a link to `/post/0x...` for the id of the post.  At the moment, those like won't work because there's not component to render the post.  Let's add that component now.

## Layout of a post with GraphQL

Adding a new component that relies on different data is a matter of adding the right query to `src/components/operations.graphql`, regenerating with GraphQL Code Generator, and then using the generated hook to layout a component.

Add a GraphQL query that gets a particular post by it's id to `src/components/operations.graphql` with this GraphQL query.

```graphql
query getPost($id: ID!) {
  getPost(id: $id) {
    id
    title
    text
    tags
    datePublished
    category {
      id
      name
    }
    author {
      username
      displayName
      avatarImg
    }
    comments {
      id
      text
      commentsOn {
        comments {
          id
          text
          author {
            username
            displayName
            avatarImg
          }
        }
      }
      author {
        username
        displayName
        avatarImg
      }
    }
  }
}
```

Then, regenerate with:

```sh
yarn run generate-types
```

...and you'll be able to use the `useGetPostQuery` hook in a component.  The difference with the previous hook is that `useGetPostQuery` relies on a variable `id` to query for a particular post.  You'll use React router's `useParams` to get the id passed to the route and then pass that to `useGetPostQuery` like this:

```js
const { id } = useParams<PostParams>()

const { data, loading, error } = useGetPostQuery({
  variables: { id: id },
})
```

Laying out the post component is then a matter of using the `data` from the hook to layout an interesting UI.  Edit the `src/components/post.tsx` component, so it lays out the post's data like this:

```js
import React from "react"
import { useParams } from "react-router-dom"
import {
  Container,
  Header,
  Loader,
  Image,
  Label,
  Comment,
} from "semantic-ui-react"
import { useGetPostQuery } from "./types/operations"
import { DateTime } from "luxon"
import { avatar } from "./avatar"

interface PostParams {
  id: string
}

export function Post() {
  const { id } = useParams<PostParams>()

  const { data, loading, error } = useGetPostQuery({
    variables: { id: id },
  })
  if (loading) return <Loader active />
  if (error) {
    return (
      <Container text className="mt-24">
        <Header as="h1">Ouch! That page didn't load</Header>
        <p>Here's why : {error.message}</p>
      </Container>
    )
  }
  if (!data?.getPost) {
    return (
      <Container text className="mt-24">
        <Header as="h1">This is not a post</Header>
        <p>You've navigated to a post that doesn't exist.</p>
        <p>That most likely means that the id {id} isn't the id of post.</p>
      </Container>
    )
  }

  let dateStr = "at some unknown time"
  if (data.getPost.datePublished) {
    dateStr =
      DateTime.fromISO(data.getPost.datePublished).toRelative() ?? dateStr
  }

  const paras = data.getPost.text.split("\n").map((str) => (
    <p key={str}>
      {str}
      <br />
    </p>
  ))

  const comments = (
    <div className="mt-3">
      {data.getPost.comments?.map((comment) => {
        return (
          <Comment.Group key={comment.id}>
            <Comment>
              <Comment.Avatar
                src={avatar(comment.author.avatarImg)}
                size="mini"
              />
              <Comment.Content>
                <Comment.Author as="a">
                  {comment.author.username}
                </Comment.Author>
                <Comment.Text>{comment.text}</Comment.Text>
              </Comment.Content>
            </Comment>
          </Comment.Group>
        )
      })}
    </div>
  )

  return (
    <div className="layout-margin">
      <div>
        <Header as="h1">{data.getPost.title} </Header>
        <span className="ui red empty mini circular label"></span>
        {" " + data.getPost?.category.name + "  "}
        {data.getPost?.tags
          ?.trim()
          .split(/\s+/)
          .map((tag) => {
            if (tag !== "") {
              return (
                <Label as="a" basic color="grey" key={tag}>
                  {tag}
                </Label>
              )
            }
          })}
      </div>
      <Header as="h4" image>
        <Image
          src={avatar(data.getPost?.author.avatarImg)}
          rounded
          size="mini"
        />
        <Header.Content>
          {data.getPost?.author.username}
          <Header.Subheader>{dateStr}</Header.Subheader>
        </Header.Content>
      </Header>
      {paras}
      {comments}
    </div>
  )
}
```

Now you can click on a post from the home screen and navigate to its page.

![post component](/images/message-board/post-component.png)

## This Step in GitHub

This step is also available in the [tutorial GitHub repo](https://github.com/dgraph-io/discuss-tutorial) with the [graphql-queries tag](https://github.com/dgraph-io/discuss-tutorial/releases/tag/graphql-queries) and is [this code diff](https://github.com/dgraph-io/discuss-tutorial/commit/db0fb435060d7369e11148054743b73fa62813f5).

If you have the app running (`yarn start`) you can navigate to `http://localhost:3000` to see the post list on the home screen and click on a post's title to navigate to the post's page.  In the diff, we've added a little extra, like the Diggy logo, that's also a link to navigate you home.
