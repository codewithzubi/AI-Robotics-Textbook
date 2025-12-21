import React from 'react';
import ChatInterface from '../ChatInterface/ChatInterface';
import styles from './AIQueryInterface.module.css';

const AIQueryInterface = () => {
  return (
    <div className={styles.aiQueryContainer}>
      <div className={styles.aiQueryHeader}>
        <h3>AI Robotics Assistant</h3>
        <p>Have a conversation with our AI about the AI Robotics textbook content.</p>
      </div>

      <ChatInterface />
    </div>
  );
};

export default AIQueryInterface;