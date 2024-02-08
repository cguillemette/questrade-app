import { useState } from "react";

interface RefreshButtonProps {
  onRefresh: () => void;
}

export const RefreshButton = ({ onRefresh }: RefreshButtonProps) => {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = () => {
    (async () => {
      try {
        setIsRefreshing(true);
        await onRefresh();
      } finally {
        setIsRefreshing(false);
      }
    })();
  }

  return (
    <button onClick={handleRefresh} disabled={isRefreshing}>
      ↺
    </button>
  );
}
