import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
      type: 'text/css',
      integrity:
        'sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM',
      crossorigin: 'anonymous',
    },
  ],
  title: 'Dgraph Documentation',
  tagline: 'The only open, complete graph database used at terabyte-scale to power real-time use cases',
  favicon: 'img/favicon-16x16.png',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://docs.dgraph.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'dgraph-io', // Usually your GitHub org/user name.
  projectName: 'dgraph-docs', // Usually your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  plugins: [
    [
      require.resolve('docusaurus-gtm-plugin'),
      {
        id: 'GTM-TZTPBZBZ',
      }
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'docs',
        path: 'docs',
        routeBasePath: '',
        sidebarPath: './sidebars.ts',
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex],
        includeCurrentVersion: false,
        lastVersion: 'v25',
        versions: {
          'v25': {
            label: 'v25.1 (latest)',
            path: '',
          },
          'v24.1': {
            label: 'v24.1',
            path: 'v24.1',
            banner: 'none',
          },
        },
        editUrl: ({versionDocsDirPath, docPath}) => {
          return `https://github.com/dgraph-io/dgraph-docs/edit/main/docusaurus-docs/${versionDocsDirPath || 'docs'}/${docPath}`;
        },
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'graphql',
        path: 'docs-graphql',
        routeBasePath: 'graphql',
        sidebarPath: './sidebars-graphql.ts',
        includeCurrentVersion: false,
        lastVersion: 'v25',
        versions: {
          'v25': {
            label: 'v25.1 (latest)',
            path: '',
          },
          'v24.1': {
            label: 'v24.1',
            path: 'v24.1',
            banner: 'none',
          },
        },
        editUrl: ({versionDocsDirPath, docPath}) => {
          return `https://github.com/dgraph-io/dgraph-docs/edit/main/docusaurus-docs/${versionDocsDirPath || 'docs-graphql'}/${docPath}`;
        },
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'ratel',
        path: 'docs-ratel',
        routeBasePath: 'ratel',
        sidebarPath: './sidebars-ratel.ts',
        editUrl: ({versionDocsDirPath, docPath}) => {
          return `https://github.com/dgraph-io/dgraph-docs/edit/main/docusaurus-docs/${versionDocsDirPath || 'docs-ratel'}/${docPath}`;
        },
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'learn',
        path: 'docs-learn',
        routeBasePath: 'learn',
        sidebarPath: './sidebars-learn.ts',
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex],
        editUrl: ({versionDocsDirPath, docPath}) => {
          return `https://github.com/dgraph-io/dgraph-docs/edit/main/docusaurus-docs/${versionDocsDirPath || 'docs-learn'}/${docPath}`;
        },
      },
    ],
  ],
  themes: [
    [
      require.resolve("@easyops-cn/docusaurus-search-local"),
      {
        hashed: true,
        indexDocs: true,
        // Index only docs, graphql, and ratel - exclude learn (tutorials)
        docsRouteBasePath: ["/", "/graphql", "/ratel"],
        searchContextByPaths: ["/", "/graphql", "/ratel"],
        language: ["en"],
        searchResultLimits: 8,
        searchBarPosition: "auto",
        forceIgnoreNoIndex: false,
        hideSearchBarWithNoSearchContext: false,
      },
    ],
  ],
  presets: [
    [
      'classic',
      {
        docs: false, // Disable default docs since we're using plugins
        blog: false, // Disable blog for now
        theme: {
          customCss: './src/css/custom.css',
        },
        googleTagManager: {
          containerId: 'GTM-TZTPBZBZ',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/dgraph-social.png',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      
      title: '',
      logo: {
        alt: 'Dgraph Logo',
        src: 'img/dgraph-light.svg',
        srcDark: 'img/dgraph-dark.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Dgraph DB',
          docId: 'overview',
          docsPluginId: 'docs',
        },
        {
          type: 'docSidebar',
          sidebarId: 'graphqlSidebar',
          position: 'left',
          label: 'GraphQL',
          docId: 'index',
          docsPluginId: 'graphql',
        },
        {
          type: 'docSidebar',
          sidebarId: 'ratelSidebar',
          position: 'left',
          label: 'Ratel UI',
          docId: 'index',
          docsPluginId: 'ratel',
        },
        {
          type: 'docSidebar',
          sidebarId: 'learnSidebar',
          position: 'left',
          label: 'Learn',
          docId: 'index',
          docsPluginId: 'learn',
        },
        {
          href: 'https://github.com/dgraph-io/dgraph',
          label: 'GitHub',
          position: 'right',
        },
        {
          type: "docsVersionDropdown",
          position: "right",
          // docsPluginId is now auto-detected by the swizzled component
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=b3287675-27fa-47c4-9f9d-5e01b7c09838" />`,
      links: [
        
      ]
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
