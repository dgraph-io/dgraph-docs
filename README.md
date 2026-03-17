# Dgraph Documentation

To read the official Dgraph documentation that is published from this repository,
please see https://docs.dgraph.io/.

## Technology Stack

This documentation site is built with [Docusaurus](https://docusaurus.io/), a modern static website generator optimized for documentation.

## Documentation Structure

The documentation is organized into four main sections, each managed by its own Docusaurus content plugin:

1. **Docs** (`/`) - Core Dgraph database documentation including DQL, administration, installation, and design concepts
2. **GraphQL** (`/graphql`) - GraphQL API documentation, schema, queries, mutations, and custom resolvers
3. **Ratel UI** (`/ratel`) - Documentation for the Ratel web-based UI tool
4. **Tutorials** (`/learn`) - Step-by-step tutorials and learning paths for different user types

Each section has its own sidebar navigation configured in:
- `sidebars.ts` - Docs sidebar
- `sidebars-graphql.ts` - GraphQL sidebar
- `sidebars-ratel.ts` - Ratel sidebar
- `sidebars-learn.ts` - Tutorials sidebar

## Running Locally

### Prerequisites

- [Node.js](https://nodejs.org/) version 20.0 or higher
- npm or yarn package manager

### Setup and Run

1. Navigate to the Docusaurus directory:
   ```bash
   cd docusaurus-docs
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

The site will automatically reload when you make changes to the documentation files.

### Build for Production

To build a production-ready static site:

```bash
npm run build
```

The built site will be in the `build/` directory. You can serve it locally with:

```bash
npm run serve
```
### Testing the current version
When testing locally you can set 
```
        includeCurrentVersion: true,
```
in the docs or graphql plugin in `docusaurus.config.ts`.

This will expose `next` in the version selector, so you can view the current (non versioned) documentation.

## Versioning

Documentation is versioned for the **docs** and **graphql** sections. Versioned content lives in:
- `docs_versioned_docs/` and `docs_versioned_sidebars/` (and `docs_versions.json`)
- `graphql_versioned_docs/` and `graphql_versioned_sidebars/` (and `graphql_versions.json`)

The folders `docs/` and `docs-graphql/` are the **“next”** (unreleased) content. They appear in the version dropdown as **“next”** only when running the site locally with `includeCurrentVersion: true` in `docusaurus.config.ts`. **When deployed, the site serves only versioned documentation** (e.g. v25.2, v25.1, v24.1); the “next” content is not shown on the live site.

**Where to edit:**

- **For the next release:** Edit the page in `docs/` or `docs-graphql/`. Those are the only places that represent the upcoming release.
- **For the current release (what’s live):** Apply the same change in the corresponding versioned folder (e.g. `docs_versioned_docs/version-v25.2/...` or `graphql_versioned_docs/version-v25.2/...` for the latest). If a fix or clarification should be in the current release, duplicate the change there.

**Note for reviewers:** The “Edit this page” link always points to the “next” page (`docs/` or `docs-graphql/`). When reviewing PRs, check whether the change should also be ported back to the current version’s versioned folder.

To create a new version:
1. Use the Docusaurus CLI: 
`npm run docusaurus docs:version:docs <version>`
`npm run docusaurus docs:version:graphql <version>`
2. This creates a new version snapshot of the current docs



## Deployment

The documentation site is automatically deployed to CloudFlare:

- **Main branch** (`main`) → Deployed to production at `https://docs.dgraph.io`
- **Preview branches** (`preview/*`) → Deployed as preview deployments for review

The deployment process is handled automatically via CloudFlare Pages integration with GitHub.

## Contribution Guidelines

As a contributor to Dgraph documentation, we ask that you do the following:
- **Label your PR for easy management**: Your PR title should be in the following format: **Topic (area): details**. The **topic** is either "Docs", "Nav" (aka, navigation), or "Chore" (for build fixes, cherry-picks, etc). The **area** is the feature (i.e. "GraphQL"), area of the docs (i.e., "Deployment"), or "Other" (for typo fixes and other bugfix PRs). So, example PR names include:
 *Docs(GraphQL): Document the @deprecated annotation* 

- **Technical writing style**: As much as possible, please follow technical writing style conventions (More on this below).

- **(Dgraph core team only)**: Include the ID of any issues/tickets related to your PR in the description (i.e., "Fixes DGRAPH-12345" or "Per DGRAPH-54321").

### Technical Writing Style

Please follow the [Dgraph Documentation Style Guide](documentation-style-guide.md) for writing conventions, formatting, and best practices.

**Note:** Please don't let these style conventions stop you from creating a PR to share your contribution to Dgraph Docs! PR reviewers can help with style guide issues.

### References

In Docusaurus, use standard Markdown links for internal references. For example, to reference a term in the glossary:


```markdown
[UID](/dgraph-glossary#uid)
```

## File Structure

```
docusaurus-docs/
├── docs/              # Main documentation content
├── docs-graphql/      # GraphQL documentation
├── docs-ratel/        # Ratel UI documentation
├── docs-learn/        # Tutorials and learning content
├── docs_versioned_docs/    # Versioned documentation snapshots
├── sidebars.ts        # Main docs sidebar configuration
├── sidebars-graphql.ts     # GraphQL sidebar configuration
├── sidebars-ratel.ts       # Ratel sidebar configuration
├── sidebars-learn.ts       # Tutorials sidebar configuration
├── docusaurus.config.ts    # Main Docusaurus configuration
└── src/               # Custom components and styles
```



