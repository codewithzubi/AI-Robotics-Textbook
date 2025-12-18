import React, { ReactNode } from 'react';
import Layout from '@theme/Layout';
import AIQueryInterface from '../AIQueryInterface/AIQueryInterface';
import styles from './AIEnhancedLayout.module.css';

interface AIEnhancedLayoutProps {
  children: ReactNode;
  title?: string;
  description?: string;
}

const AIEnhancedLayout: React.FC<AIEnhancedLayoutProps> = ({
  children,
  title = 'AI Robotics Textbook',
  description = 'A comprehensive textbook on modern robotics, AI, and humanoid systems'
}) => {
  return (
    <Layout title={title} description={description}>
      <div className={styles.aiEnhancedContainer}>
        <main className={styles.mainContent}>
          {children}
        </main>
        <aside className={styles.aiSidebar}>
          <div className={styles.aiInterfaceContainer}>
            <AIQueryInterface />
          </div>
        </aside>
      </div>
    </Layout>
  );
};

export default AIEnhancedLayout;