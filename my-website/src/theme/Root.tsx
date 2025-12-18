import React, { useEffect } from 'react';
import AIFloatingButton from '../components/AIFloatingButton/AIFloatingButton';

// Default theme wrapper
const Root = ({ children }) => {
  return (
    <>
      {children}
      <AIFloatingButton />
    </>
  );
};

export default Root;