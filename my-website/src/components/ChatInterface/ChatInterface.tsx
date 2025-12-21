import React, { useState, useRef, useEffect, KeyboardEvent } from 'react';
import styles from './ChatInterface.module.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: string[];
  confidence_score?: number;
  processing_time_ms?: number;
}

interface ChatInterfaceProps {
  apiUrl?: string;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ apiUrl = 'https://zubair0077-ai-robotics-text-book.hf.space/api/v1/agent' }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${apiUrl}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          max_tokens: 500,
          temperature: 0.7,
          metadata: {
            source: 'docusaurus-chat-frontend',
          }
        }),
      });

      const data = await response.json();

      if (data.status === 'success' && data.data) {
        const aiMessage: Message = {
          id: Date.now().toString(),
          role: 'assistant',
          content: data.data.answer,
          timestamp: new Date(),
          sources: data.data.sources,
          confidence_score: data.data.confidence_score,
          processing_time_ms: data.data.processing_time_ms
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        const errorMessage: Message = {
          id: Date.now().toString(),
          role: 'assistant',
          content: data.error?.message || 'Sorry, I encountered an error processing your request.',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (err) {
      console.error('Error submitting query:', err);
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Failed to connect to the AI service. Please make sure the backend is running.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as unknown as React.FormEvent);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chatHeader}>
        <h3>AI Robotics Assistant</h3>
        <button onClick={clearChat} className={styles.clearChatButton}>
          Clear Chat
        </button>
      </div>

      <div className={styles.messagesContainer}>
        {messages.length === 0 ? (
          <div className={styles.welcomeMessage}>
            <h4>Ask me anything about AI Robotics!</h4>
            <p>I can help explain concepts, provide examples, and answer questions about the textbook content.</p>
          </div>
        ) : (
          <div className={styles.messagesList}>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${styles[message.role]}`}
              >
                <div className={styles.messageContent}>
                  {message.role === 'assistant' && (
                    <div className={styles.messageHeader}>
                      <div className={styles.botIcon}>🤖</div>
                      <span className={styles.senderName}>AI Assistant</span>
                    </div>
                  )}

                  <div className={styles.content}>
                    {message.content.split('\n').map((paragraph, index) => (
                      <p key={index}>{paragraph}</p>
                    ))}
                  </div>

                  {message.role === 'assistant' && message.sources && message.sources.length > 0 && (
                    <div className={styles.sourcesSection}>
                      <h5>Sources:</h5>
                      <ul>
                        {message.sources.map((source, idx) => (
                          <li key={idx}>{source}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {message.role === 'assistant' && message.confidence_score !== undefined && (
                    <div className={styles.metadata}>
                      <span className={styles.confidenceScore}>
                        Confidence: {(message.confidence_score * 100).toFixed(1)}%
                      </span>
                      {message.processing_time_ms && (
                        <span className={styles.processingTime}>
                          Processed in {(message.processing_time_ms / 1000).toFixed(2)}s
                        </span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.messageContent}>
                  <div className={styles.messageHeader}>
                    <div className={styles.botIcon}>🤖</div>
                    <span className={styles.senderName}>AI Assistant</span>
                  </div>
                  <div className={styles.typingIndicator}>
                    <div className={styles.dot}></div>
                    <div className={styles.dot}></div>
                    <div className={styles.dot}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}

        {error && (
          <div className={styles.errorMessage}>
            <p>{error}</p>
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className={styles.inputContainer}>
        <textarea
          ref={textareaRef}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={(e) => handleKeyDown(e as unknown as KeyboardEvent<HTMLTextAreaElement>)}
          placeholder="Type your message here..."
          className={styles.textInput}
          rows={1}
          disabled={isLoading}
        />
        <button
          type="submit"
          className={styles.sendButton}
          disabled={isLoading || !inputValue.trim()}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;