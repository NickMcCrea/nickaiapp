import React from 'react';
import './StatusUpdater.css';

interface StatusUpdaterProps {
  statusText: string; // This prop holds the status text to display
  isComplete: boolean; // This prop determines if the animation should be running
}

const StatusUpdater: React.FC<StatusUpdaterProps> = ({ statusText, isComplete }) => {
  // The component now directly uses the props instead of internal state

  return (
    <div className={`status-updater ${isComplete ? 'complete' : 'animated'}`}>
      {statusText}
    </div>
  );
};

export default StatusUpdater;
