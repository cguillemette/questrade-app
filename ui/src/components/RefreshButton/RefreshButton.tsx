import { useState } from 'react';
import './RefreshButton.css';

interface RefreshButtonProps {
  onRefresh: () => void;
}

export const RefreshButton = ({ onRefresh }: RefreshButtonProps) => {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = async () => {
    try {
      setIsRefreshing(true);
      await onRefresh();
    } finally {
      setIsRefreshing(false);
    }
  }

  return (
    <button onClick={handleRefresh} disabled={isRefreshing}>
      <div className={isRefreshing ? 'spinning' : '' }>↺</div>
    </button>
  );
}
