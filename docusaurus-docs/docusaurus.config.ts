import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Dgraph Documentation',
  tagline: 'The only open, complete graph database used at terabyte-scale to power real-time use cases',
  favicon: 'img/favicon-16x16.png',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://dgraph.io',
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
      '@docusaurus/plugin-content-docs',
      {
        id: 'docs',
        path: 'docs',
        routeBasePath: '',
        sidebarPath: './sidebars.ts',
        editUrl: 'https://github.com/dgraph-io/dgraph-docs/tree/main/',
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'graphql',
        path: 'docs-graphql',
        routeBasePath: 'graphql',
        sidebarPath: './sidebars-graphql.ts',
        editUrl: 'https://github.com/dgraph-io/dgraph-docs/tree/main/',
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'ratel',
        path: 'docs-ratel',
        routeBasePath: 'ratel',
        sidebarPath: './sidebars-ratel.ts',
        editUrl: 'https://github.com/dgraph-io/dgraph-docs/tree/main/',
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'learn',
        path: 'docs-learn',
        routeBasePath: 'learn',
        sidebarPath: './sidebars-learn.ts',
        editUrl: 'https://github.com/dgraph-io/dgraph-docs/tree/main/',
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
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
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
          label: 'Tutorials',
          docId: 'index',
          docsPluginId: 'learn',
        },
        {
          href: 'https://github.com/dgraph-io/dgraph',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
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
