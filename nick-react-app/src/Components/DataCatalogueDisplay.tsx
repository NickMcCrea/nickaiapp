import React from 'react';
import './DataSourceCatalogueDisplay.css'; // Path to your CSS file for styling both components
import RestaurantIcon from '@mui/icons-material/Restaurant';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import StorageIcon from '@mui/icons-material/Storage';

// Define a type for the DataSourceCard props
type DataSourceCardProps = {
  dataSourceName: string;
};

// Define the DataSourceCard component
const DataSourceCard: React.FC<DataSourceCardProps> = ({ dataSourceName }) => {
  // Function to determine which icon to use
  const getIcon = (dataSourceName: string) => {
    if (dataSourceName.toLowerCase().includes('restaurant')) {
      return <RestaurantIcon className="icon" />;
    } else if (dataSourceName.toLowerCase().includes('spotify') || dataSourceName.toLowerCase().includes('track')) {
      return <MusicNoteIcon className="icon" />;
    } else {
      return <StorageIcon className="icon" />;
    }
  };

  return (
    <div className="data-source-card">
      <div className="icon-container">{getIcon(dataSourceName)}</div>
      <h3>{dataSourceName}</h3>
    </div>
  );
};

// Define a type for the DataSourceCatalogueDisplay props
type DataSourceCatalogueDisplayProps = {
  dataSources: string[];
  commentary: string;
};

// Define the DataSourceCatalogueDisplay component
const DataSourceCatalogueDisplay: React.FC<DataSourceCatalogueDisplayProps> = ({ dataSources, commentary }) => {
  return (
    <div className="data-source-catalogue-display">
      <h2>{commentary}</h2>
      <div className="data-source-cards-container">
        {dataSources.map((dataSource, index) => (
          <DataSourceCard
            key={index}
            dataSourceName={dataSource}
          />
        ))}
      </div>
    </div>
  );
};

export default DataSourceCatalogueDisplay;
