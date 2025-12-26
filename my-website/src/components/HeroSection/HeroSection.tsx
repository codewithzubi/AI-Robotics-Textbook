import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './HeroSection.module.css';

const HeroSection: React.FC = () => {
  const {siteConfig} = useDocusaurusContext();

  return (
    <section className={styles.hero}>
      <div className={styles.container}>
        {/* Left side: Content */}
        <div className={styles.content}>
          <h1 className={styles.title}>
            {siteConfig.title}
          </h1>
          <p className={styles.subtitle}>
            Explore the world of AI-driven humanoid robotics from fundamentals to advanced applications.
          </p>
          <div className={styles.verticalButtonContainer}>
            <Link
              className={clsx('button button--primary button--lg', styles.startButton)}
              to="/docs/intro">
              Start Learning
            </Link>
            <Link
              className={clsx('button button--secondary button--lg', styles.secondaryButton)}
              to="/docs/getting-started">
              Getting Started
            </Link>
          </div>
        </div>

        {/* Right side: Image */}
        <div className={styles.illustration}>
          <img
            src="/img/img-for-hero-section.jpg"
            alt="AI Robotics Hero Section"
            className={styles.heroImage}
          />
        </div>
      </div>
    </section>
  );  
};

export default HeroSection;