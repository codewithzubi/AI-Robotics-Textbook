import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';


interface SearchContextType {
  isSearchModalOpen: boolean;
  openSearchModal: () => void;
  closeSearchModal: () => void;
  performSearch: (query: string) => void;
}

const SearchContext = createContext<SearchContextType | undefined>(undefined);

export const SearchProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isSearchModalOpen, setIsSearchModalOpen] = useState(false);

  // Handle keyboard shortcuts (Ctrl+K or Cmd+K)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Check for Ctrl+K or Cmd+K
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        if (isSearchModalOpen) {
          closeSearchModal();
        } else {
          openSearchModal();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isSearchModalOpen]);

  const openSearchModal = () => {
    setIsSearchModalOpen(true);
  };

  const closeSearchModal = () => {
    setIsSearchModalOpen(false);
  };

  const performSearch = useCallback((query: string) => {
    // Navigate to the AI chat page with the query
    console.log('Performing search for:', query);

    // Close the modal after search
    closeSearchModal();

    // Redirect to the AI chat page with the query as a parameter
    // This will allow the AI to respond based on the book content
    window.location.href = `${window.location.origin}/ai?query=${encodeURIComponent(query)}`;
  }, [closeSearchModal]);

  return (
    <SearchContext.Provider
      value={{
        isSearchModalOpen,
        openSearchModal,
        closeSearchModal,
        performSearch,
      }}
    >
      {children}
    </SearchContext.Provider>
  );
};

export const useSearch = () => {
  const context = useContext(SearchContext);
  if (context === undefined) {
    throw new Error('useSearch must be used within a SearchProvider');
  }
  return context;
};