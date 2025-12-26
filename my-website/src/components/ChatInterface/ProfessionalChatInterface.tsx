import React, { useState, useRef, useEffect, KeyboardEvent, useCallback } from 'react';
import styles from './ProfessionalChatInterface.module.css';

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
  searchQuery?: string;
}

const ProfessionalChatInterface: React.FC<ChatInterfaceProps> = ({
  apiUrl = 'https://zubair0077-ai-robotics-text-book.hf.space/api/v1/agent',
  searchQuery
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Handle search queries passed from parent component
  useEffect(() => {
    if (searchQuery && searchQuery.trim()) {
      setInputValue(searchQuery);
      // Auto-submit if we have a search query
      setTimeout(() => {
        handleSubmit(new Event('submit') as unknown as React.FormEvent);
      }, 100);
    }
  }, [searchQuery]);

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

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={styles.chatContainer}>
      {/* Chat Header */}
      <div className={styles.chatHeader}>
        <div className={styles.headerContent}>
          <div className={styles.assistantInfo}>
            <div className={styles.assistantAvatar}>
              <span className={styles.assistantIcon}>🤖</span>
            </div>
            <div className={styles.assistantDetails}>
              <h3 className={styles.assistantName}>AI Robotics Assistant</h3>
              <p className={styles.assistantStatus}>
                <span className={styles.statusIndicator}></span>
                <span className={styles.statusText}>Online</span>
              </p>
            </div>
          </div>
          <button onClick={clearChat} className={styles.clearChatButton}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
            <span>Clear Chat</span>
          </button>
        </div>
      </div>

      {/* Messages Container */}
      <div className={styles.messagesContainer}>
        {messages.length === 0 ? (
          <div className={styles.welcomeContainer}>
            <div className={styles.welcomeContent}>
              <div className={styles.welcomeIcon}>
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
              </div>
              <h2 className={styles.welcomeTitle}>Welcome to AI Robotics Assistant</h2>
              <p className={styles.welcomeSubtitle}>
                Ask me anything about AI Robotics, ROS, Digital Twin Simulation, NVIDIA Isaac, or Vision-Language-Action systems.
                I can help explain concepts, provide examples, and answer questions about the textbook content.
              </p>
              <div className={styles.welcomeFeatures}>
                <div className={styles.featureCard}>
                  <div className={styles.featureIcon}>📚</div>
                  <h4>Concept Explanations</h4>
                  <p>Get detailed explanations of robotics concepts</p>
                </div>
                <div className={styles.featureCard}>
                  <div className={styles.featureIcon}>💡</div>
                  <h4>Code Examples</h4>
                  <p>Find practical code examples and implementations</p>
                </div>
                <div className={styles.featureCard}>
                  <div className={styles.featureIcon}>❓</div>
                  <h4>Q&A Support</h4>
                  <p>Ask questions about the textbook content</p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className={styles.messagesList}>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${styles[message.role]}`}
              >
                <div className={styles.messageWrapper}>
                  <div className={styles.messageAvatar}>
                    {message.role === 'user' ? (
                      <div className={styles.userAvatar}>
                        <span className={styles.userIcon}>👤</span>
                      </div>
                    ) : (
                      <div className={styles.assistantAvatar}>
                        <span className={styles.assistantIcon}>🤖</span>
                      </div>
                    )}
                  </div>

                  <div className={styles.messageBubble}>
                    <div className={styles.messageContent}>
                      {message.content.split('\n').map((paragraph, index) => (
                        <p key={index} className={styles.messageParagraph}>{paragraph}</p>
                      ))}
                    </div>

                    {message.role === 'assistant' && message.sources && message.sources.length > 0 && (
                      <div className={styles.sourcesSection}>
                        <div className={styles.sourcesHeader}>
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                            <line x1="16" y1="13" x2="8" y2="13"></line>
                            <line x1="16" y1="17" x2="8" y2="17"></line>
                            <polyline points="10 9 9 9 8 9"></polyline>
                          </svg>
                          <span>Sources</span>
                        </div>
                        <ul className={styles.sourcesList}>
                          {message.sources.map((source, idx) => (
                            <li key={idx} className={styles.sourceItem}>{source}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {message.role === 'assistant' && message.confidence_score !== undefined && (
                      <div className={styles.messageMetadata}>
                        <span className={styles.confidenceScore}>
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                          </svg>
                          Confidence: {(message.confidence_score * 100).toFixed(1)}%
                        </span>
                        {message.processing_time_ms && (
                          <span className={styles.processingTime}>
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                              <circle cx="12" cy="12" r="10"></circle>
                              <polyline points="12 6 12 12 16 14"></polyline>
                            </svg>
                            {(message.processing_time_ms / 1000).toFixed(2)}s
                          </span>
                        )}
                      </div>
                    )}

                    <div className={styles.messageTime}>
                      {formatTime(message.timestamp)}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.messageWrapper}>
                  <div className={styles.messageAvatar}>
                    <div className={styles.assistantAvatar}>
                      <span className={styles.assistantIcon}>🤖</span>
                    </div>
                  </div>
                  <div className={`${styles.messageBubble} ${styles.typingBubble}`}>
                    <div className={styles.typingIndicator}>
                      <div className={styles.dot}></div>
                      <div className={styles.dot}></div>
                      <div className={styles.dot}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className={styles.inputContainer}>
        {error && (
          <div className={styles.errorMessage}>
            <div className={styles.errorContent}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <span>{error}</span>
              <button onClick={() => setError(null)} className={styles.closeError}>
                ×
              </button>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className={styles.messageForm}>
          <div className={styles.inputWrapper}>
            <textarea
              ref={textareaRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => handleKeyDown(e as unknown as KeyboardEvent<HTMLTextAreaElement>)}
              placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
              className={styles.textInput}
              rows={1}
              disabled={isLoading}
            />
            <button
              type="submit"
              className={`${styles.sendButton} ${inputValue.trim() ? styles.active : ''}`}
              disabled={isLoading || !inputValue.trim()}
            >
              {isLoading ? (
                <svg className={styles.spinner} width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <circle className={styles.spinnerPath} cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="22" y1="2" x2="11" y2="13"></line>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProfessionalChatInterface;