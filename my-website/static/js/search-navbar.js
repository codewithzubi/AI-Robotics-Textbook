// Search functionality for navbar button using event delegation
document.addEventListener('DOMContentLoaded', function() {
  // Use event delegation to handle clicks on the search button
  document.addEventListener('click', function(e) {
    const target = e.target;
    if (target && target instanceof HTMLElement && target.id === 'search-navbar-btn') {
      // Prevent any default behavior
      e.preventDefault();
      e.stopPropagation();

      // Dispatch a custom event that React components can listen to
      window.dispatchEvent(new CustomEvent('openSearchModal'));
    } else if (target && target instanceof HTMLElement && target.closest && target.closest('#search-navbar-btn')) {
      // Also check if the click was on a child of the search button
      e.preventDefault();
      e.stopPropagation();
      window.dispatchEvent(new CustomEvent('openSearchModal'));
    }
  });

  // Handle keyboard shortcut (Ctrl+K or Cmd+K)
  document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      window.dispatchEvent(new CustomEvent('openSearchModal'));
    }
  });
});

// Also add the event listener in case DOM is loaded after script
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function() {
    // Event delegation is already set up above
  });
} else {
  // DOM is already loaded, set up event listeners immediately
  document.addEventListener('click', function(e) {
    const target = e.target;
    if (target && target instanceof HTMLElement && target.id === 'search-navbar-btn') {
      e.preventDefault();
      e.stopPropagation();
      window.dispatchEvent(new CustomEvent('openSearchModal'));
    } else if (target && target instanceof HTMLElement && target.closest && target.closest('#search-navbar-btn')) {
      e.preventDefault();
      e.stopPropagation();
      window.dispatchEvent(new CustomEvent('openSearchModal'));
    }
  });

  document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      window.dispatchEvent(new CustomEvent('openSearchModal'));
    }
  });
}