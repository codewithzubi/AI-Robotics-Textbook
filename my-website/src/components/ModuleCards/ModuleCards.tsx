import type {ReactNode} from 'react';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import styles from './ModuleCards.module.css';

type Module = {
  title: string;
  description: string;
  link: string;
};

function ModuleCards(): ReactNode {
  const modules: Module[] = [
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
    <section className={styles.modulesSection}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>Textbook Modules</Heading>
        <div className={styles.modulesGrid}>
          {modules.map((module, index) => {
            // Define unique icons for each module
            let moduleIcon;
            switch(index) {
              case 0: // ROS 2 Foundations
                moduleIcon = (
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                  </svg>
                );
                break;
              case 1: // Digital Twin Simulation
                moduleIcon = (
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                  </svg>
                );
                break;
              case 2: // NVIDIA Isaac Robotics AI
                moduleIcon = (
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" strokeWidth="2"/>
                    <path d="M8 12h8M12 8v8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  </svg>
                );
                break;
              case 3: // Vision-Language-Action Systems
                moduleIcon = (
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                  </svg>
                );
                break;
              default:
                moduleIcon = (
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                  </svg>
                );
            }

            return (
              <Link
                key={index}
                to={module.link}
                className={styles.moduleCardLink}
                aria-label={`Learn more about ${module.title}`}
              >
                <div className={styles.moduleCard}>
                  {/* Card image/icon */}
                  <div className={styles.cardImageContainer}>
                    <div className={styles.cardIconBackground}>
                      <div className={styles.moduleIcon}>
                        {moduleIcon}
                      </div>
                    </div>
                  </div>

                  {/* Card content */}
                  <Heading as="h3" className={styles.cardTitle}>{module.title}</Heading>
                  <p className={styles.cardDescription}>{module.description}</p>

                  {/* Learn more arrow */}
                  <div className={styles.learnMoreArrow}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M5 12h14"></path>
                      <path d="M12 5l7 7-7 7"></path>
                    </svg>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </section>
  );
}

export default ModuleCards;