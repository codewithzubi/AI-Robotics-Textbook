import React, { createContext, useContext, useState, useEffect } from 'react';

interface UserProfileContextType {
  isProfileDropdownOpen: boolean;
  openProfileDropdown: () => void;
  closeProfileDropdown: () => void;
  toggleProfileDropdown: () => void;
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  language: 'en' | 'ur';
  setLanguage: (language: 'en' | 'ur') => void;
}

const UserProfileContext = createContext<UserProfileContextType | undefined>(undefined);

export const UserProfileProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isProfileDropdownOpen, setIsProfileDropdownOpen] = useState(false);
  const [theme, setThemeState] = useState<'light' | 'dark'>('dark');
  const [language, setLanguageState] = useState<'en' | 'ur'>('en');

  // Handle the custom event from the navbar
  useEffect(() => {
    const handleToggleUserProfile = () => {
      setIsProfileDropdownOpen(prev => !prev);
    };

    window.addEventListener('openUserProfile', handleToggleUserProfile);

    return () => {
      window.removeEventListener('openUserProfile', handleToggleUserProfile);
    };
  }, []);

  // Handle theme change
  const setTheme = (newTheme: 'light' | 'dark') => {
    setThemeState(newTheme);
    localStorage.setItem('theme', newTheme);

    // Apply theme to document
    if (newTheme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
    }
  };

  // Handle language change
  const setLanguage = (newLanguage: 'en' | 'ur') => {
    setLanguageState(newLanguage);
    localStorage.setItem('language', newLanguage);

    // In a real app, you would update the UI text here
    console.log(`Language changed to: ${newLanguage}`);
  };

  // Load saved theme and language on component mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null;
    const savedLanguage = localStorage.getItem('language') as 'en' | 'ur' | null;

    if (savedTheme && (savedTheme === 'light' || savedTheme === 'dark')) {
      setThemeState(savedTheme);
      if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
      } else {
        document.documentElement.setAttribute('data-theme', 'light');
      }
    }

    if (savedLanguage && (savedLanguage === 'en' || savedLanguage === 'ur')) {
      setLanguageState(savedLanguage);
    }
  }, []);

  const openProfileDropdown = () => {
    setIsProfileDropdownOpen(true);
  };

  const closeProfileDropdown = () => {
    setIsProfileDropdownOpen(false);
  };

  const toggleProfileDropdown = () => {
    setIsProfileDropdownOpen(prev => !prev);
  };

  return (
    <UserProfileContext.Provider
      value={{
        isProfileDropdownOpen,
        openProfileDropdown,
        closeProfileDropdown,
        toggleProfileDropdown,
        theme,
        setTheme,
        language,
        setLanguage,
      }}
    >
      {children}
    </UserProfileContext.Provider>
  );
};

export const useUserProfile = () => {
  const context = useContext(UserProfileContext);
  if (context === undefined) {
    throw new Error('useUserProfile must be used within a UserProfileProvider');
  }
  return context;
};