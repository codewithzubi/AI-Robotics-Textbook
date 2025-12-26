import React, { useState, useEffect, useRef, KeyboardEvent } from 'react';
import ReactDOM from 'react-dom';
import styles from './SearchModal.module.css';
import { getSuggestions, searchContent, getDetailedSuggestions, SearchSuggestion } from '../../services/searchIndex';

interface SearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSearch: (query: string) => void;
}

const SearchModal: React.FC<SearchModalProps> = ({ isOpen, onClose, onSearch }) => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [detailedSuggestions, setDetailedSuggestions] = useState<SearchSuggestion[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const modalRef = useRef<HTMLDivElement>(null);

  // Focus input when modal opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Close modal on Escape key
  useEffect(() => {
    const handleKeyDown = (e: React.KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown as any);
      return () => document.removeEventListener('keydown', handleKeyDown as any);
    }
    // Explicitly return undefined when condition is false
    return undefined;
  }, [isOpen, onClose]);

  // Close modal when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: globalThis.MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(e.target as Node)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
    // Explicitly return undefined when condition is false
    return undefined;
  }, [isOpen, onClose]);

  // Fetch suggestions from the book content with proper debouncing
  useEffect(() => {
    let isActive = true; // Flag to check if component is still mounted

    if (query.length > 0) {
      setIsLoading(true);

      // Use a debounce mechanism to avoid too many requests
      const timer = setTimeout(async () => {
        if (isActive) { // Only proceed if component is still mounted
          try {
            const suggestions = await getSuggestions(query);
            const detailedSugs = await getDetailedSuggestions(query);
            if (isActive) { // Only update state if component is still mounted
              setSuggestions(suggestions);
              setDetailedSuggestions(detailedSugs);
            }
          } catch (error) {
            console.error('Error fetching suggestions:', error);
            if (isActive) { // Only update state if component is still mounted
              // Fallback to empty array if there's an error
              setSuggestions([]);
              setDetailedSuggestions([]);
            }
          } finally {
            if (isActive) {
              setIsLoading(false);
            }
          }
        }
      }, 300);

      return () => {
        isActive = false; // Set flag to false when effect is cleaned up
        clearTimeout(timer);
      };
    } else {
      setSuggestions([]);
      setDetailedSuggestions([]);
      setIsLoading(false);
    }
    // Explicitly return undefined
    return undefined;
  }, [query]); // Only re-run when query changes

  const handleSearch = async () => {
    if (query.trim()) {
      setIsLoading(true);
      try {
        // Call the parent component's search function
        onSearch(query.trim());
      } finally {
        setIsLoading(false);
        setQuery('');
        setSuggestions([]);
        // Ensure input maintains focus after search completes
        setTimeout(() => {
          if (inputRef.current) {
            inputRef.current.focus();
          }
        }, 0);
      }
    }
  };

  const handleSuggestionClick = async (suggestionTitle: string) => {
    // Find the matching content for the suggestion from detailed suggestions
    const matchingDetailedSuggestion = detailedSuggestions.find(item => item.title === suggestionTitle);

    if (matchingDetailedSuggestion) {
      // If we found a matching item, navigate directly to it
      // For Docusaurus, we should update the window location to the doc path
      window.location.href = window.location.origin + matchingDetailedSuggestion.url;
      onClose(); // Close the modal after navigation
    } else {
      // Find the matching content from search results
      const searchResults = await searchContent(suggestionTitle);
      const matchingItem = searchResults.find(item => item.title === suggestionTitle);

      if (matchingItem) {
        // If we found a matching item, navigate directly to it
        window.location.href = window.location.origin + matchingItem.url;
        onClose(); // Close the modal after navigation
      } else {
        // If no specific match found, set the query for AI processing
        // Update the query but don't clear suggestions yet - user might want to see more
        setQuery(suggestionTitle);
        // Clear suggestions after setting the query to avoid flickering
        setSuggestions([]);
        // Keep focus on input so user can continue typing or press enter
        setTimeout(() => {
          if (inputRef.current) {
            inputRef.current.focus();
            // Move cursor to end of text
            const length = suggestionTitle.length;
            inputRef.current.setSelectionRange(length, length);
          }
        }, 0);

        // Trigger the search with the suggestion for AI processing
        onSearch(suggestionTitle);
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && suggestions[selectedIndex]) {
        handleSuggestionClick(suggestions[selectedIndex]);
      } else {
        handleSearch();
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(prev => Math.min(prev + 1, suggestions.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(prev => Math.max(prev - 1, -1));
    }
  };

  const handleVoiceSearch = () => {
    // Use the Web Speech API for voice recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognition();

      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setQuery(transcript);
      };

      recognition.onerror = (event: any) => {
        console.error('Speech recognition error', event.error);
      };

      recognition.start();
    } else {
      alert('Your browser does not support speech recognition. Please try a modern browser like Chrome.');
    }
  };

  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className={styles.overlay}>
      <div className={styles.modal} ref={modalRef}>
        <div className={styles.searchContainer}>
          <div className={styles.searchInputContainer}>
            <span className={styles.searchIcon}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.3-4.3"></path>
              </svg>
            </span>
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => {
                // Store cursor position before state update
                const cursorPosition = e.target.selectionStart;
                const inputValue = e.target.value;

                setQuery(inputValue);
                setSelectedIndex(-1); // Reset selection when typing

                // Restore cursor position after state update
                setTimeout(() => {
                  if (inputRef.current) {
                    inputRef.current.focus();
                    inputRef.current.setSelectionRange(cursorPosition, cursorPosition);
                  }
                }, 0);
              }}
              onKeyDown={handleKeyDown}
              placeholder="Search the textbook..."
              className={styles.searchInput}
              disabled={isLoading}
            />
            <button
              onClick={handleVoiceSearch}
              className={styles.voiceButton}
              aria-label="Voice search"
              disabled={isLoading}
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                <line x1="12" y1="19" x2="12" y2="23"></line>
                <line x1="8" y1="23" x2="16" y2="23"></line>
              </svg>
            </button>
          </div>

          {detailedSuggestions.length > 0 && (
            <div className={styles.suggestionsContainer}>
              {detailedSuggestions.map((suggestion, index) => (
                <div
                  key={index}
                  className={`${styles.suggestionItem} ${index === selectedIndex ? styles.selected : ''}`}
                  onClick={() => handleSuggestionClick(suggestion.title)}
                >
                  <div className={styles.suggestionTitle}>{suggestion.title}</div>
                  <div className={styles.suggestionPreview}>{suggestion.contentPreview}</div>
                </div>
              ))}
            </div>
          )}

          {isLoading && (
            <div className={styles.loading}>
              <div className={styles.spinner}></div>
              <span>Searching...</span>
            </div>
          )}
        </div>

        <button
          onClick={onClose}
          className={styles.closeButton}
          aria-label="Close search"
          disabled={isLoading}
        >
          ×
        </button>
      </div>
    </div>,
    document.body
  );
};

export default SearchModal;