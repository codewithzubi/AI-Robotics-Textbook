import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx(styles.heroBanner)}>
      <div className="container">
        <div className={styles.homepageLayoutCentered}>
          <div className={styles.textContentCentered}>
            <div className={styles.heroContent}>
              <Heading as="h1" className="hero__title">
                {siteConfig.title}
              </Heading>
              <p className="hero__subtitle">{siteConfig.tagline}</p>
              <div className={styles.buttonsCentered}>
                <Link
                  className="button button--secondary button--lg"
                  to="/docs/intro">
                 Button 1
                </Link>
                <Link
                  className="button button--secondary button--lg"
                  to="/docs/intro">
                 Button 2
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function ModelCardsSection() {
  const modules = [
    {
      title: "ROS 2 Foundations",
      description: "Learn the fundamentals of Robot Operating System 2 for building robust robotics applications.",
      link: "/docs/modules/module-1-ros-foundations"
    },
    {
      title: "Digital Twin Simulation",
      description: "Explore digital twin technologies for simulating and testing robotic systems in virtual environments.",
      link: "/docs/modules/module-2-digital-twin-simulation"
    },
    {
      title: "NVIDIA Isaac Robotics AI",
      description: "Master NVIDIA's Isaac platform for AI-powered robotics and autonomous systems.",
      link: "/docs/modules/module-3-nvidia-isaac-ai"
    },
    {
      title: "Vision-Language-Action Systems",
      description: "Understand how visual perception, language processing, and action control integrate in robotics.",
      link: "/docs/modules/module-4-vla-systems"
    }
  ];

  return (
    <section className={styles.modelsSection}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>Textbook Modules</Heading>
        <div className={styles.modelsGrid}>
          {modules.map((module, index) => (
            <Link key={index} to={module.link} className={styles.modelCardLink}>
              <div className={styles.modelCard}>
                <div className={styles.modelImage}>
                  <div className={styles.placeholderImage}></div>
                </div>
                <Heading as="h3" className={styles.modelTitle}>{module.title}</Heading>
                <p className={styles.modelDescription}>{module.description}</p>
              </div>
            </Link>
          ))}
        </div>
        <div className={styles.sectionButton}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Click and Whatever, whichever model you like best
          </Link>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="A comprehensive textbook on modern robotics, AI, and humanoid systems">
      <HomepageHeader />
      <ModelCardsSection />
    </Layout>
  );
}
