import React, { useState, useRef, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { useUserProfile } from '../../contexts/UserProfileContext';
import styles from './ProfessionalUserProfileNavbarItem.module.css';
import type { Props } from '@theme/NavbarItem/DefaultNavbarItem';
import { FaUser, FaBook, FaGraduationCap, FaCog, FaSignOutAlt, FaBell, FaChartBar } from 'react-icons/fa';

const ProfessionalUserProfileNavbarItem: React.FC<Props> = (props) => {
  const { isProfileDropdownOpen, toggleProfileDropdown } = useUserProfile();
  const [isHovered, setIsHovered] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node) &&
          buttonRef.current && !buttonRef.current.contains(event.target as Node)) {
        // Close the dropdown if it's open and click is outside
        if (isProfileDropdownOpen) {
          toggleProfileDropdown();
        }
      }
    };

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        toggleProfileDropdown();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscape);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isProfileDropdownOpen, toggleProfileDropdown]);

  // Handle logout
  const handleLogout = () => {
    console.log('User logged out');
    // In a real app, you would handle actual logout logic here
    toggleProfileDropdown();
  };

  // Calculate position for dropdown to appear below the navbar button
  const calculatePosition = () => {
    if (buttonRef.current) {
      const buttonRect = buttonRef.current.getBoundingClientRect();
      return {
        top: `${buttonRect.bottom + window.scrollY}px`,
        right: `${window.innerWidth - buttonRect.right}px`,
      };
    }
    return { top: '60px', right: '20px' }; // fallback position
  };

  const position = calculatePosition();

  return (
    <div style={{ display: 'flex', alignItems: 'center' }}>
      <button
        ref={buttonRef}
        className={`${styles.profileButton} ${isHovered ? styles.hovered : ''}`}
        onClick={toggleProfileDropdown}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        aria-haspopup="true"
        aria-expanded={isProfileDropdownOpen}
        aria-label="User profile menu"
      >
        <div className={styles.avatarContainer}>
          <div className={styles.avatarInitial}>U</div>
        </div>
      </button>

      {isProfileDropdownOpen && ReactDOM.createPortal(
        <div className={styles.dropdownOverlay}>
          <div
            className={styles.dropdown}
            ref={dropdownRef}
            style={{ top: position.top, right: position.right }}
          >
            {/* User Profile Header */}
            <div className={styles.profileHeader}>
              <div className={styles.avatarLarge}>
                <div className={styles.avatarInitialLarge}>U</div>
              </div>
              <div className={styles.userInfo}>
                <div className={styles.userName}>User Name</div>
                <div className={styles.userEmail}>user@example.com</div>
                <div className={styles.userRole}>Student</div>
              </div>
            </div>

            {/* User Stats */}
            <div className={styles.userStats}>
              <div className={styles.statItem}>
                <FaBook className={styles.statIcon} />
                <span className={styles.statNumber}>12</span>
                <span className={styles.statLabel}>Modules</span>
              </div>
              <div className={styles.statItem}>
                <FaGraduationCap className={styles.statIcon} />
                <span className={styles.statNumber}>24</span>
                <span className={styles.statLabel}>Completed</span>
              </div>
              <div className={styles.statItem}>
                <FaChartBar className={styles.statIcon} />
                <span className={styles.statNumber}>85%</span>
                <span className={styles.statLabel}>Progress</span>
              </div>
            </div>

            {/* Dropdown Menu */}
            <div className={styles.dropdownMenu}>
              {/* Profile */}
              <button
                className={styles.menuItem}
                onClick={() => {
                  console.log('Profile clicked');
                  toggleProfileDropdown();
                }}
              >
                <span className={styles.menuItemContent}>
                  <FaUser className={styles.menuIcon} />
                  <span>My Profile</span>
                </span>
              </button>

              {/* Learning Progress */}
              <button
                className={styles.menuItem}
                onClick={() => {
                  console.log('Learning progress clicked');
                  toggleProfileDropdown();
                }}
              >
                <span className={styles.menuItemContent}>
                  <FaGraduationCap className={styles.menuIcon} />
                  <span>Learning Progress</span>
                </span>
              </button>

              {/* Notifications */}
              <button
                className={styles.menuItem}
                onClick={() => {
                  console.log('Notifications clicked');
                  toggleProfileDropdown();
                }}
              >
                <span className={styles.menuItemContent}>
                  <FaBell className={styles.menuIcon} />
                  <span>Notifications</span>
                </span>
              </button>

              {/* Settings */}
              <button
                className={styles.menuItem}
                onClick={() => {
                  console.log('Settings clicked');
                  toggleProfileDropdown();
                }}
              >
                <span className={styles.menuItemContent}>
                  <FaCog className={styles.menuIcon} />
                  <span>Settings</span>
                </span>
              </button>

              {/* Divider */}
              <div className={styles.divider}></div>

              {/* Logout */}
              <button
                className={`${styles.menuItem} ${styles.logoutButton}`}
                onClick={handleLogout}
              >
                <span className={styles.menuItemContent}>
                  <FaSignOutAlt className={styles.menuIcon} />
                  <span>Logout</span>
                </span>
              </button>
            </div>
          </div>
        </div>,
        document.body
      )}
    </div>
  );
};

export default ProfessionalUserProfileNavbarItem;