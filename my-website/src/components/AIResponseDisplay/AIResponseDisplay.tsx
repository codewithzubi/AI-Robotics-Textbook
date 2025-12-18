import React from 'react';
import type { AgentResponse } from '../../types/ai-agent-types';
import styles from './AIResponseDisplay.module.css';

interface AIResponseDisplayProps {
  response: AgentResponse;
}

const AIResponseDisplay: React.FC<AIResponseDisplayProps> = ({ response }) => {
  return (
    <div className={styles.responseContainer}>
      <div className={styles.responseHeader}>
        <h4>AI Response</h4>
        <div className={styles.responseMetadata}>
          <span className={styles.confidenceScore}>
            Confidence: {(response.confidence_score * 100).toFixed(1)}%
          </span>
          <span className={styles.processingTime}>
            Processed in {(response.processing_time_ms / 1000).toFixed(2)}s
          </span>
        </div>
      </div>

      <div className={styles.responseContent}>
        {response.answer.split('\n').map((paragraph, index) => (
          <p key={index} style={{ color: '#111827', fontSize: '1rem', lineHeight: '1.6' }}>{paragraph}</p>
        ))}
      </div>

      {response.sources && response.sources.length > 0 && (
        <div className={styles.sourcesSection}>
          <h5>Sources:</h5>
          <ul>
            {response.sources.map((source, index) => (
              <li key={index}>{source}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default AIResponseDisplay;