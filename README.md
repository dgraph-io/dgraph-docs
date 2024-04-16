# Dgraph Documentation

To read the official Dgraph documentation that is published from this repository,
please see https://dgraph.io/docs/.

## Contribution guidelines

As a contributor to Dgraph documentation, we ask that you do the following:
- **Label your PR for easy management**: Your PR title should be in the following format: **Topic (area): details**. The **topic** is either "Docs", "Nav" (aka, navigation), or "Chore" (for build fixes, cherry-picks, etc). The **area** is the feature (i.e. "GraphQL"), area of the docs (i.e., "Deployment"), or "Other" (for typo fixes and other bugfix PRs). So, example PR names include:
 *Docs(GraphQL): Document the @deprecated annotation* or *Chore(Other): cherry-pick updates from master to release/v20.11*
- **Develop in the `master` branch first**: Make any changes applicable to the current (recently-released) version of Dgraph in the `master` branch first, and then cherry-pick those changes to the correct release branch (for example, `release/v20.11`).

 **Exception**: Changes that *only* apply to older Dgraph versions (for example `release/v20.07`), can occur directly in a release branch, but will not be cherry-picked forward.
- **Note planned cherry-pick(s) in your PR description**: If you are creating a PR in `master` and you know it needs to be cherry-picked to a release branch, please mention that in your PR description (for example: "cherry-pick to v20.07"). Cherry-pick PRs should reference the original PR.

- **Link to discuss.dgraph.io posts when applicable**: If your PR is based on discussions on [Discuss](https://discuss.dgraph.io), feel free to include a link to the relevant discussion in your PR description.

- **Technical writing style**: As much as possible, please follow [technical writing style](#technical-writing-style) conventions (More on this below).

- **(Dgraph core team only)**: Include the ID of any issues/tickets related to your PR in the description (i.e., "Fixes DGRAPH-12345" or "Per DGRAPH-54321").

### Technical writing style

Dgraph Labs uses a style guide for our documentation so that we can make it as easy to understand as possible. The [Dgraph Style Guide](https://discuss.dgraph.io/t/dgraph-developer-documentation-style-guide/10955) is a concise style reference for our documentation, but it isn't comprehensive. For anything not found in our style guide, use Google's [Developer Docs Style Guide](https://developers.google.com/style/highlights).

#### Style tips for machine-translatable docs!

Making our documentation easy to understand includes optimizing it for client-side machine translation into other languages. To help with this, please see the following technical writing style tips:
- Generally, use the second person ("you") rather than the third-person ("the developer") when addressing the reader.
- Always use the third person when describing Dgraph database or features (avoid "this lets us" in favor of "this lets Dgraph").
- Write in present-tense, active voice when you can.
- Prefer simple sentences to complex and complex-compound sentences.

**Note:** Please don't let these style conventions stop you from creating a PR to share your contribution to Dgraph Docs! PR reviewers can help with style guide issues.

### Staging doc updates locally

We use [Hugo](https://gohugo.io/) for our documentation. You can use Hugo to locally stage doc updates before or after creating a PR.

1. Download and install the latest patch of hugo version v0.79.x from [here](https://github.com/gohugoio/hugo/releases/).
   ```bash
   pushd ~/Downloads
   VERSION=v0.79
   TAG=$(curl -s https://api.github.com/repos/gohugoio/hugo/releases | jq '.[].tag_name' -r | grep $VERSION | head -1)
   OS=$(uname -s)
   if [[ ${OS,,} == "darwin" ]]; then
     PKG=hugo_${TAG##v}_macOS-64bit.tar.gz
     curl -sLO https://github.com/gohugoio/hugo/releases/download/${TAG}/${PKG}
     tar xvzf $PKG hugo
     sudo mv hugo /usr/local/bin/
   else
     PKG=hugo_${TAG##v}_Linux-64bit.deb
     curl -sLO https://github.com/gohugoio/hugo/releases/download/${TAG}/${PKG}
     sudo apt install $PKG
   fi
   popd
   ```
2. Run the command below to get the theme.
   ```bash
   pushd themes && git clone https://github.com/dgraph-io/hugo-docs && popd
   ```
3. Run `./scripts/local.sh` and visit [http://localhost:1313](http://localhost:1313) to see the documentation site running on your local machine.

(Optional) To run queries _within_ the documentation using a different Dgraph instance, set the `DGRAPH_ENDPOINT` environment variable before starting the local web server:

```bash
DGRAPH_ENDPOINT="http://localhost:8080/query?latency=true" ./scripts/local.sh
```

Now you can make changes to the docs and see them being updated instantly, thanks to Hugo.

**Note**: While running locally, the version selector does not work because you need to build the documentation and serve it behind a reverse proxy to have multiple versions. Also, formatting of lists is less fussy when running locally; so please precede lists with a blank line in your PR.

### Running docs locally with Docker

Make sure you have docker-compose installed.

Run:

```sh
sh scripts/docker.sh
```

### Branch

Depending on what branch you are on, some code examples will dynamically change.
For example, `go-grpc` code examples will have different import path depending
on the branch name.

## Runnable code examples

Some code examples are runnable, allowing for reader interaction with a data set.

### Custom example

Pass custom Go-GRPC example to the runnable by passing a `customExampleGoGRPC` to the `runnable` shortcode.

```
{{< runnable
  customExampleGoGRPC="this\nis\nan example"
>}}{
  director(func:allofterms(name, "steven spielberg")) {
    name@en
    director.film (orderdesc: initial_release_date) {
      name@en
      initial_release_date
    }
  }
}
{{< /runnable >}}
```

**Note:** Runnable doesn't support passing a multiline string as an argument to a shortcode. Therefore, you have to create the whole custom example in a single line string by replacing newlines with `\n`.

## History
add Hypermode banner by updating the hugo-docs repository with topbat template.