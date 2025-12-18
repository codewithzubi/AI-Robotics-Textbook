import React, { useState, useRef, useEffect } from 'react';
import styles from './AIQueryInterface.module.css';
import AIResponseDisplay from '../AIResponseDisplay/AIResponseDisplay';
import type { QueryRequest, AgentResponse, APIResponse } from '../../types/ai-agent-types';

const AIQueryInterface = () => {
  const [query, setQuery] = useState<string>('');
  const [response, setResponse] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedText, setSelectedText] = useState<string>('');
  const [useSelectedText, setUseSelectedText] = useState<boolean>(true);
  const [isContextAvailable, setIsContextAvailable] = useState<boolean>(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Get the API base URL - using a default for local development
  // In production, this could be configured differently
  const API_BASE_URL = 'http://localhost:8000/api/v1/agent';

  // Function to get selected text from the page
  const getSelectedText = (): string => {
    return window.getSelection?.()?.toString()?.trim() || '';
  };

  // Handle text selection on the page
  useEffect(() => {
    const handleSelection = () => {
      const selected = getSelectedText();
      setSelectedText(selected);
      setIsContextAvailable(selected.length > 0);
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, []);

  // Function to submit query to the backend
  const submitQuery = async () => {
    if (!query.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      // Prepare the query - include selected text if user wants to use it as context
      let finalQuery = query;
      if (useSelectedText && selectedText) {
        finalQuery = `Context: "${selectedText}"\n\nQuestion: ${query}`;
      }

      const queryRequest: QueryRequest = {
        query: finalQuery,
        max_tokens: 500,
        temperature: 0.7,
        metadata: {
          source: 'docusaurus-frontend',
          selected_text_length: selectedText.length,
          use_context: useSelectedText && selectedText.length > 0
        }
      };

      const response = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(queryRequest),
      });

      const data: APIResponse = await response.json();

      if (data.status === 'success' && data.data) {
        setResponse(data.data as AgentResponse);
      } else {
        setError(data.error?.message || 'An error occurred while processing your query');
      }
    } catch (err) {
      console.error('Error submitting query:', err);
      setError('Failed to connect to the AI agent service. Please make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    submitQuery();
  };

  // Handle keydown for Enter (but allow Shift+Enter for new line)
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submitQuery();
    }
  };

  return (
    <div className={styles.aiQueryContainer}>
      <div className={styles.aiQueryHeader}>
        <h3>Ask AI about the Textbook</h3>
        <p>Ask questions about the AI Robotics content. Select text on the page for context-aware answers.</p>
      </div>

      {isContextAvailable && (
        <div className={styles.contextInfo}>
          <div className={styles.contextPreview}>
            <strong>Context:</strong> "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
          </div>
          <div className={styles.contextToggle}>
            <label>
              <input
                type="checkbox"
                checked={useSelectedText}
                onChange={(e) => setUseSelectedText(e.target.checked)}
              />
              Use selected text as context
            </label>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className={styles.queryForm}>
        <div className={styles.queryInputContainer}>
          <textarea
            ref={textareaRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about the AI Robotics textbook content..."
            className={styles.queryInput}
            rows={3}
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          className={styles.queryButton}
          disabled={loading || !query.trim()}
        >
          {loading ? 'Thinking...' : 'Ask AI'}
        </button>
      </form>

      {loading && (
        <div className={styles.loadingIndicator}>
          <div className={styles.spinner}></div>
          <p>AI is processing your question...</p>
        </div>
      )}

      {error && (
        <div className={styles.errorContainer}>
          <p className={styles.errorText}>{error}</p>
          <button
            onClick={() => setError(null)}
            className={styles.closeError}
          >
            ×
          </button>
        </div>
      )}

      {response && (
        <AIResponseDisplay response={response} />
      )}
    </div>
  );
};

export default AIQueryInterface;