import React, { useEffect } from 'react';
import { useSearch } from '../../contexts/SearchContext';
import { useUserProfile } from '../../contexts/UserProfileContext';
import SearchModal from '../SearchModal/SearchModal';
import { getSuggestions, getContentById } from '../../services/searchIndex';

const GlobalSearchModal: React.FC = () => {
  const { isSearchModalOpen, closeSearchModal, openSearchModal, performSearch } = useSearch();
  const { toggleProfileDropdown } = useUserProfile();

  // Handle the custom event from the navbar for search
  useEffect(() => {
    const handleOpenSearchModal = () => {
      openSearchModal(); // This opens the search modal
    };

    window.addEventListener('openSearchModal', handleOpenSearchModal);

    return () => {
      window.removeEventListener('openSearchModal', handleOpenSearchModal);
    };
  }, [openSearchModal]);

  // Handle the custom event from the navbar for user profile
  useEffect(() => {
    const handleOpenUserProfile = () => {
      toggleProfileDropdown(); // This toggles the user profile dropdown
    };

    window.addEventListener('openUserProfile', handleOpenUserProfile);

    return () => {
      window.removeEventListener('openUserProfile', handleOpenUserProfile);
    };
  }, [toggleProfileDropdown]);

  const handleSearch = (query: string) => {
    performSearch(query);
  };

  return (
    <SearchModal
      isOpen={isSearchModalOpen}
      onClose={closeSearchModal}
      onSearch={handleSearch}
    />
  );
};

export default GlobalSearchModal;