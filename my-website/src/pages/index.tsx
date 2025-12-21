import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import HeroSection from '../components/HeroSection/HeroSection';
import ModuleCards from '../components/ModuleCards/ModuleCards';

import styles from './index.module.css';

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="A comprehensive textbook on modern robotics, AI, and humanoid systems">
      <HeroSection />
      <ModuleCards />
    </Layout>
  );
}
