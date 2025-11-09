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

## Versioning

Docusaurus supports documentation versioning. Versioned documentation is stored in:
- `docs_versioned_docs/` - Versioned docs content
- `docs_versioned_sidebars/` - Versioned sidebar configurations
- `docs_versions.json` - Version metadata

The version dropdown in the navbar automatically detects which documentation section you're viewing and shows the appropriate versions. Currently, versioning is configured for the main `docs` section.

To create a new version:
1. Use the Docusaurus CLI: `npm run docusaurus docs:version <version>`
2. This creates a new version snapshot of the current docs

## Deployment

The documentation site is automatically deployed to CloudFlare:

- **Main branch** (`main`) → Deployed to production at `https://docs.dgraph.io`
- **Preview branches** (`preview/*`) → Deployed as preview deployments for review

The deployment process is handled automatically via CloudFlare Pages integration with GitHub.

## Contribution Guidelines

As a contributor to Dgraph documentation, we ask that you do the following:
- **Label your PR for easy management**: Your PR title should be in the following format: **Topic (area): details**. The **topic** is either "Docs", "Nav" (aka, navigation), or "Chore" (for build fixes, cherry-picks, etc). The **area** is the feature (i.e. "GraphQL"), area of the docs (i.e., "Deployment"), or "Other" (for typo fixes and other bugfix PRs). So, example PR names include:
 *Docs(GraphQL): Document the @deprecated annotation* or *Chore(Other): cherry-pick updates from main to release/v20.11*
- **Develop in the `main` branch first**: Make any changes applicable to the current (recently-released) version of Dgraph in the `main` branch first, and then cherry-pick those changes to the correct release branch (for example, `release/v20.11`).

 **Exception**: Changes that *only* apply to older Dgraph versions (for example `release/v20.07`), can occur directly in a release branch, but will not be cherry-picked forward.
- **Note planned cherry-pick(s) in your PR description**: If you are creating a PR in `main` and you know it needs to be cherry-picked to a release branch, please mention that in your PR description (for example: "cherry-pick to v20.07"). Cherry-pick PRs should reference the original PR.

- **Link to discuss.dgraph.io posts when applicable**: If your PR is based on discussions on Discuss, feel free to include a link to the relevant discussion in your PR description.

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

## Testing

### Type Checking

Run TypeScript type checking:

```bash
npm run typecheck
```

### Link Checking

After building the site, you can check for broken links using external tools or by manually testing the built site.

## Runnable Code Examples

Some code examples in the documentation are interactive and runnable, allowing readers to execute queries directly in the browser. These are implemented using custom Docusaurus components.
