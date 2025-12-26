import React, { useState, useEffect } from 'react';
import { useSearch } from '../../contexts/SearchContext';
import ChatInterface from '../ChatInterface/ProfessionalChatInterface';
import styles from './AIQueryInterface.module.css';

const AIQueryInterface: React.FC = () => {
  const { performSearch: contextPerformSearch } = useSearch();
  const [searchQuery, setSearchQuery] = useState<string | undefined>(undefined);

  // Check URL for query parameter on component mount
  useEffect(() => {
    // First check URL search parameters
    const urlParams = new URLSearchParams(window.location.search);
    let queryParam = urlParams.get('query');

    if (!queryParam) {
      // Also check if query is in the hash part (for backward compatibility)
      const hash = window.location.hash;
      if (hash.includes('?query=')) {
        const hashParams = new URLSearchParams(hash.split('?')[1]);
        queryParam = hashParams.get('query');
      }
    }

    if (queryParam) {
      const decodedQuery = decodeURIComponent(queryParam);
      setSearchQuery(decodedQuery);
    }

    // Listen for hash changes to detect new queries
    const handleHashChange = () => {
      const hash = window.location.hash;
      if (hash.includes('?query=')) {
        const hashParams = new URLSearchParams(hash.split('?')[1]);
        const queryParam = hashParams.get('query');
        if (queryParam) {
          const decodedQuery = decodeURIComponent(queryParam);
          setSearchQuery(decodedQuery);
        }
      }
    };

    window.addEventListener('hashchange', handleHashChange);
    return () => {
      window.removeEventListener('hashchange', handleHashChange);
    };
  }, []);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    contextPerformSearch(query);
  };

  return (
    <div className={styles.aiQueryContainer}>
      <div className={styles.aiQueryHeader}>
        <h3>AI Robotics Assistant</h3>
        <p>Have a conversation with our AI about the AI Robotics textbook content.</p>
      </div>

      <ChatInterface searchQuery={searchQuery} />
    </div>
  );
};

export default AIQueryInterface;