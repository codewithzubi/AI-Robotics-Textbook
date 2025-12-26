import React from 'react';
import { SearchProvider } from '../contexts/SearchContext';
import { UserProfileProvider } from '../contexts/UserProfileContext';
import AIFloatingButton from '../components/AIFloatingButton/AIFloatingButton';
import GlobalSearchModal from '../components/GlobalSearchModal/GlobalSearchModal';

// Default theme wrapper
const Root: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <UserProfileProvider>
      <SearchProvider>
        {children}
        <GlobalSearchModal />
        <AIFloatingButton />
      </SearchProvider>
    </UserProfileProvider>
  );
};

export default Root;