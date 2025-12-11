import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  learnSidebar: [
    'index',
    {
      type: 'category',
      label: 'Developer',
      items: [
        'developer/index',
        {
          type: 'category',
          label: 'Todo App Tutorial',
          items: [
            'developer/todo-app-tutorial/index',
            'developer/todo-app-tutorial/todo-overview',
            'developer/todo-app-tutorial/todo-schema-design',
            'developer/todo-app-tutorial/todo-UI',
            'developer/todo-app-tutorial/todo-auth-rules',
            'developer/todo-app-tutorial/todo-auth0-jwt',
            'developer/todo-app-tutorial/todo-firebase-jwt',
            'developer/todo-app-tutorial/todo-deploy',
          ],
        },
        {
          type: 'category',
          label: 'React',
          items: [
            'developer/react/index',
            'developer/react/react-introduction',
            {
              type: 'category',
              label: 'GraphQL',
              items: [
                'developer/react/graphql/index',
                'developer/react/graphql/design-app-schema',
                'developer/react/graphql/graphql-schema',
                'developer/react/graphql/load-schema-to-dgraph-cloud',
                'developer/react/graphql/graphql-operations',
                'developer/react/graphql/react-graphql-mutations',
                'developer/react/graphql/react-graphql-queries',
              ],
            },
            {
              type: 'category',
              label: 'React UI',
              items: [
                'developer/react/react-ui/index',
                'developer/react/react-ui/tech-stack',
                'developer/react/react-ui/react-app-boiler-plate',
                'developer/react/react-ui/connect-to-dgraph-cloud',
                'developer/react/react-ui/react-routing',
                'developer/react/react-ui/react-ui-graphql-queries',
                'developer/react/react-ui/react-ui-graphql-mutations',
              ],
            },
            'developer/react/react-conclusion',
          ],
        },
        {
          type: 'category',
          label: 'Sample Apps',
          items: [
            'developer/sample-apps/index',
            'developer/sample-apps/charts',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Data Engineer',
      items: [
        'data-engineer/index',
        {
          type: 'category',
          label: 'Get Started with Dgraph',
          items: [
            'data-engineer/get-started-with-dgraph/index',
            'data-engineer/get-started-with-dgraph/tutorial-1/index',
            'data-engineer/get-started-with-dgraph/tutorial-2/index',
            'data-engineer/get-started-with-dgraph/tutorial-3/index',
            'data-engineer/get-started-with-dgraph/tutorial-4/index',
            'data-engineer/get-started-with-dgraph/tutorial-5/index',
            'data-engineer/get-started-with-dgraph/tutorial-6/index',
            'data-engineer/get-started-with-dgraph/tutorial-7/index',
            'data-engineer/get-started-with-dgraph/tutorial-8/index',
          ],
        },
        {
          type: 'category',
          label: 'Data Model 101',
          items: [
            'data-engineer/data-model-101/index',
            'data-engineer/data-model-101/dm-101-introduction',
            'data-engineer/data-model-101/relational-data-model',
            'data-engineer/data-model-101/graph-data-model',
            'data-engineer/data-model-101/rel-query',
            'data-engineer/data-model-101/graph-query',
            'data-engineer/data-model-101/dm-101-conclusion',
          ],
        },
        'data-engineer/analytical-power-dgraph',
      ],
    },
    {
      type: 'category',
      label: 'Administrator',
      items: [
        'administrator/index',
      ],
    },
    {
      type: 'category',
      label: 'How To',
      link: {
        type: 'doc',
        id: 'howto/index',
      },
      items: [
        'howto/completion',
        'howto/concurrent-modification-java-multithreaded',
        'howto/dgraph-sentry-integration',
        'howto/dql-schema-request',
        'howto/drop-data',
        'howto/jepsen-tests',
        'howto/load-balancing-nginx',
        'howto/login-system',
        'howto/retrieving-debug-information',
        'howto/similarity-search',
        'howto/using-debug-tool',
        'howto/using-increment-tool',
        {
          type: 'category',
          label: 'Command Line',
          link: {
            type: 'doc',
            id: 'howto/commandline/index',
          },
          items: [
            'howto/commandline/about-cli',
            'howto/commandline/create-cli',
          ],
        },
      ],
    },
  ],
};

export default sidebars;
