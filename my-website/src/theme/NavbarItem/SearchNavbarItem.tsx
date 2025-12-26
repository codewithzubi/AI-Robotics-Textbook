import React, { useEffect } from 'react';
import { useSearch } from '../../contexts/SearchContext';
import type { Props } from '@theme/NavbarItem/DefaultNavbarItem';

const SearchNavbarItem: React.FC<Props> = () => {
  const { openSearchModal } = useSearch();

  // Handle keyboard shortcut (Ctrl+K or Cmd+K)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        openSearchModal();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [openSearchModal]);

  return (
    <button
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
        openSearchModal();
      }}
      className="navbar__item navbar__link"
      aria-label="Search"
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: '42px',
        height: '42px',
        borderRadius: '50%',
        background: 'transparent',
        border: 'none',
        cursor: 'pointer',
        fontSize: '20px',
        color: 'var(--ifm-navbar-link-color)',
        transition: 'background-color 0.2s ease',
        margin: '0 0.5rem',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.backgroundColor = 'var(--ifm-color-emphasis-200)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.backgroundColor = 'transparent';
      }}
    >
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="11" cy="11" r="8"></circle>
        <path d="m21 21-4.3-4.3"></path>
      </svg>
    </button>
  );
};

export default SearchNavbarItem;