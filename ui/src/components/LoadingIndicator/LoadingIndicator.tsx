import React, { ReactNode } from 'react';
import './LoadingIndicator.css';

interface LoadingIndicatorProps {
  loading: boolean;
  children: ReactNode;
}

export const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({ loading, children }) => {
  return (
    <div className={`${loading ? 'loading' : ''}`}>
      {children}
    </div>
  );
};
