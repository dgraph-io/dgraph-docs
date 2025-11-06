# Dgraph Documentation - Docusaurus

This directory contains the Docusaurus-based documentation site. The original Hugo content remains in the `content/` directory at the root of the repository and is not modified.

## Structure

The documentation is organized into 4 main tabs matching the Hugo structure:

- `docs/` - Dgraph DB (main documentation, route: `/dgraph-overview`)
- `docs-graphql/` - GraphQL API documentation (route: `/graphql`)
- `docs-ratel/` - Ratel UI documentation (route: `/ratel`)
- `docs-learn/` - Tutorials documentation (route: `/learn`)

Each section has its own sidebar configuration in `sidebars-*.ts` files:
- `sidebars.ts` - Dgraph DB sidebar
- `sidebars-graphql.ts` - GraphQL sidebar
- `sidebars-ratel.ts` - Ratel UI sidebar
- `sidebars-learn.ts` - Tutorials sidebar

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Build for production:
   ```bash
   npm run build
   ```

4. Serve the built site:
   ```bash
   npm run serve
   ```

## Configuration

The main configuration is in `docusaurus.config.ts`. Each documentation section is configured as a separate docs plugin instance with its own:
- `path` - Directory containing the markdown files
- `routeBasePath` - URL path for the section
- `sidebarPath` - Sidebar configuration file

## Migration Status

Currently, only the overview/index pages have been migrated from Hugo. More content will be migrated gradually.

## Hugo Content

The original Hugo content remains untouched in `../content/` and can still be built with Hugo using the original build process.
