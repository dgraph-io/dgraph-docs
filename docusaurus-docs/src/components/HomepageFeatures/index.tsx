import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type CardItem = {
  title: string;
  description: ReactNode;
  link: string;
  icon: ReactNode;
};

const CardList: CardItem[] = [
  {
    title: 'Dgraph DB',
    description: 'Get started, use and operate Dgraph database.',
    link: '/dgraph-overview',
    icon: (
      <svg className={styles.cardIcon} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M21.9995 14.6L21.9995 20.4C21.9995 20.7314 21.7309 21 21.3995 21L17.5995 21C17.2681 21 16.9995 20.7314 16.9995 20.4L16.9995 14.6C16.9995 14.2686 17.2681 14 17.5995 14L21.3995 14C21.7309 14 21.9995 14.2686 21.9995 14.6Z" stroke="#100C19" strokeWidth="1.33333"/>
        <path d="M6.99951 9.1L6.99951 14.9C6.99951 15.2314 6.73088 15.5 6.39951 15.5L2.59951 15.5C2.26814 15.5 1.99951 15.2314 1.99951 14.9L1.99951 9.1C1.99951 8.76863 2.26814 8.5 2.59951 8.5L6.39951 8.5C6.73088 8.5 6.99951 8.76863 6.99951 9.1Z" stroke="#EF265A" strokeWidth="1.33333"/>
        <path d="M21.9995 3.6L21.9995 9.4C21.9995 9.73137 21.7309 10 21.3995 10L17.5995 10C17.2681 10 16.9995 9.73137 16.9995 9.4L16.9995 3.6C16.9995 3.26863 17.2681 3 17.5995 3L21.3995 3C21.7309 3 21.9995 3.26863 21.9995 3.6Z" stroke="#100C19" strokeWidth="1.33333"/>
        <path d="M16.9995 17.5L13.4995 17.5C12.3949 17.5 11.4995 16.6046 11.4995 15.5L11.4995 8.5C11.4995 7.3954 12.3949 6.5 13.4995 6.5L16.9995 6.5" stroke="#100C19" strokeWidth="1.33333"/>
        <path d="M11.4995 12L6.99951 12" stroke="#100C19" strokeWidth="1.33333"/>
      </svg>
    ),
  },
  {
    title: 'GraphQL API',
    description: 'Generate a GraphQL API and a graph backend from your GraphQL schema.',
    link: '/graphql',
    icon: (
      <svg className={styles.cardIcon} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M2.52691 17.6612L3.37109 18.1592L12.7756 1.51639L11.9315 1.01839L2.52691 17.6612Z" fill="#100C19"/>
        <path d="M21.1509 16.332H2.3418V17.328H21.1509V16.332Z" fill="#100C19"/>
        <path d="M2.71302 16.8914L12.1211 22.4414L12.6085 21.5789L3.20042 16.0289L2.71302 16.8914Z" fill="#100C19"/>
        <path d="M10.8888 2.42656L20.2969 7.97656L20.7843 7.11403L11.3762 1.56403L10.8888 2.42656Z" fill="#100C19"/>
        <path d="M2.71181 7.11012L3.19922 7.97266L12.6073 2.42266L12.1199 1.56012L2.71181 7.11012Z" fill="#100C19"/>
        <path d="M10.7107 1.51639L20.1152 18.1592L20.9594 17.6612L11.5549 1.01839L10.7107 1.51639Z" fill="#100C19"/>
        <path d="M4.0627 6.44922H3.08789V17.5492H4.0627V6.44922Z" fill="#100C19"/>
        <path d="M20.4104 6.4502H19.4355V17.5502H20.4104V6.4502Z" fill="#100C19"/>
        <path d="M11.5235 21.2661L11.9492 22.0195L20.1317 17.1925L19.706 16.4391L11.5235 21.2661Z" fill="#100C19"/>
        <path d="M21.6995 17.874C21.1357 18.876 19.879 19.218 18.8984 18.642C17.9177 18.066 17.583 16.782 18.1467 15.78C18.7104 14.778 19.9671 14.436 20.9478 15.012C21.9344 15.594 22.2691 16.872 21.6995 17.874Z" fill="#EF265A"/>
        <path d="M5.34009 8.21973C4.77635 9.22173 3.51967 9.56373 2.53899 8.98773C1.55831 8.41173 1.22358 7.12773 1.78733 6.12573C2.35107 5.12373 3.60775 4.78173 4.58843 5.35773C5.56911 5.93973 5.90384 7.21773 5.34009 8.21973Z" fill="#EF265A"/>
        <path d="M1.79319 17.874C1.22944 16.872 1.56416 15.594 2.54485 15.012C3.52553 14.436 4.77634 14.778 5.34595 15.78C5.9097 16.782 5.57497 18.06 4.59429 18.642C3.60774 19.218 2.35693 18.876 1.79319 17.874Z" fill="#EF265A"/>
        <path d="M18.1545 8.21973C17.5908 7.21773 17.9255 5.93973 18.9062 5.35773C19.8869 4.78173 21.1377 5.12373 21.7073 6.12573C22.271 7.12773 21.9363 8.40573 20.9556 8.98773C19.9749 9.56373 18.7183 9.22173 18.1545 8.21973Z" fill="#EF265A"/>
        <path d="M11.7487 23.7476C10.6153 23.7476 9.69922 22.8116 9.69922 21.6536C9.69922 20.4956 10.6153 19.5596 11.7487 19.5596C12.882 19.5596 13.7981 20.4956 13.7981 21.6536C13.7981 22.8056 12.882 23.7476 11.7487 23.7476Z" fill="#EF265A"/>
        <path d="M11.7487 4.43995C10.6153 4.43995 9.69922 3.50395 9.69922 2.34595C9.69922 1.18795 10.6153 0.251953 11.7487 0.251953C12.882 0.251953 13.7981 1.18795 13.7981 2.34595C13.7981 3.50395 12.882 4.43995 11.7487 4.43995Z" fill="#EF265A"/>
      </svg>
    ),
  },
];

function Card({title, description, link, icon}: CardItem) {
  return (
    <div className={clsx('col col--6')}>
      <Link to={link} className={styles.card}>
        <div className={styles.cardIconWrapper}>
          {icon}
        </div>
        <Heading as="h2" className={styles.cardTitle}>{title}</Heading>
        <p className={styles.cardDescription}>{description}</p>
      </Link>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.intro}>
          <p>
            Dgraph is the only open, complete graph database used at terabyte-scale to power real-time use cases. It is open-source, scalable, distributed, highly available and lightning fast.
          </p>
          <p>
            Dgraph is designed for real-time workloads, horizontal scalability, and data
            flexibility. Implemented as a distributed system, Dgraph processes queries in
            parallel to deliver the fastest results, even for the most complex workloads.
          </p>
          <Heading as="h3">Choose your path</Heading>
          <p>Use Dgraph as a <strong>property graph database</strong> for direct database operations and administration,<br /> or leverage the <strong>GraphQL API</strong> for rapid application development with schema-driven APIs.</p>
        </div>
        <div className="row">
          {CardList.map((props, idx) => (
            <Card key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
