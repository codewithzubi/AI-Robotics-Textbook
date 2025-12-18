import React, { useState } from 'react';
import AIQueryInterface from '../AIQueryInterface/AIQueryInterface';
import styles from './AIFloatingButton.module.css';

const AIFloatingButton = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(true);

  const toggleInterface = () => {
    if (!isOpen) {
      setIsOpen(true);
      setIsMinimized(false);
    } else {
      setIsMinimized(!isMinimized);
    }
  };

  const closeInterface = () => {
    setIsOpen(false);
    setIsMinimized(true);
  };

  return (
    <>
      {isOpen && (
        <div className={styles.overlay} onClick={closeInterface}></div>
      )}

      <div className={`${styles.aiFloatingContainer} ${isOpen ? styles.open : ''} ${isMinimized ? styles.minimized : ''}`}>
        {isMinimized ? (
          <button
            className={styles.aiFloatingButton}
            onClick={toggleInterface}
            title="Ask AI about this page"
          >
            <span className={styles.aiIcon}>🤖</span>
            <span>AI Assistant</span>
          </button>
        ) : (
          <div className={styles.aiInterfaceWrapper}>
            <div className={styles.aiHeader}>
              <h4>AI Assistant</h4>
              <div className={styles.aiHeaderActions}>
                <button
                  className={styles.minimizeButton}
                  onClick={() => setIsMinimized(true)}
                  title="Minimize"
                >
                  −
                </button>
                <button
                  className={styles.closeButton}
                  onClick={closeInterface}
                  title="Close"
                >
                  ×
                </button>
              </div>
            </div>
            <div className={styles.aiInterfaceContent}>
              <AIQueryInterface />
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default AIFloatingButton;