import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './HeroSection.module.css';

const HeroSection = () => {
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
          <div className={styles.buttonContainer}>
            <Link
              className={clsx('button button--primary button--lg', styles.startButton)}
              to="/docs/intro">
              Start Learning
            </Link>
          </div>
        </div>

        {/* Right side: Image/Illustration */}
        <div className={styles.illustration}>
          <div className={styles.robotImage}>
            {/* Placeholder for robot illustration - can be replaced with actual SVG or image */}
            <svg
              viewBox="0 0 400 300"
              className={styles.robotSvg}
              aria-label="Futuristic humanoid robot illustration"
            >
              {/* Robot head */}
              <circle cx="200" cy="80" r="40" fill="#4a5568" />

              {/* Robot eyes */}
              <circle cx="185" cy="75" r="6" fill="#00d4ff" />
              <circle cx="215" cy="75" r="6" fill="#00d4ff" />

              {/* Robot body */}
              <rect x="170" y="120" width="60" height="80" rx="10" fill="#2d3748" />

              {/* Robot arms */}
              <rect x="140" y="130" width="30" height="10" rx="5" fill="#2d3748" />
              <rect x="230" y="130" width="30" height="10" rx="5" fill="#2d3748" />

              {/* Robot legs */}
              <rect x="175" y="200" width="15" height="40" rx="5" fill="#2d3748" />
              <rect x="210" y="200" width="15" height="40" rx="5" fill="#2d3748" />

              {/* Tech details */}
              <circle cx="200" cy="160" r="8" fill="#00d4ff" opacity="0.7" />
              <circle cx="190" cy="140" r="4" fill="#00d4ff" opacity="0.5" />
              <circle cx="210" cy="140" r="4" fill="#00d4ff" opacity="0.5" />
            </svg>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;