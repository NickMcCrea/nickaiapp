import React from 'react';
import './DataSourceCatalogueDisplay.css'; // Path to your CSS file for styling both components
import RestaurantIcon from '@mui/icons-material/Restaurant';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import StorageIcon from '@mui/icons-material/Storage';

// Define the shape of the accumulator object
interface CategoryAccumulator {
  [key: string]: DataSourceMetaDeta[];
}

// Define a type for the DataSourceCard props
type DataSourceCardProps = {
  dataSource: DataSourceMetaDeta;
};

// Define the DataSourceCard component
const DataSourceCard: React.FC<DataSourceCardProps> = ({ dataSource }) => {
  // Function to determine which icon to use
  const getIcon = (name: string) => {
    if (name.toLowerCase().includes('restaurant')) {
      return <RestaurantIcon className="icon" />;
    } else if (name.toLowerCase().includes('spotify') || name.toLowerCase().includes('track')) {
      return <MusicNoteIcon className="icon" />;
    } else {
      return <StorageIcon className="icon" />;
    }
  };

  return (
    <div className="data-source-card">
      <div className="icon-container">{getIcon(dataSource.name)}</div>
      <h3>{dataSource.name}</h3>
      <p>{dataSource.description}</p> {/* Optional: Display description */}
    </div>
  );
};

// New component to represent a category of data sources
const DataSourceCategory: React.FC<{ category: string; dataSources: DataSourceMetaDeta[] }> = ({ category, dataSources }) => {
  return (
    <div className="data-source-category">
      <h3 className="category-title">{category}</h3>
      <div className="data-source-cards-container">
        {dataSources.map((dataSource, index) => (
          <DataSourceCard
            key={index}
            dataSource={dataSource}
          />
        ))}
      </div>
    </div>
  );
};

export interface DataSourceMetaDeta {
  name: string;
  description: string;
  category: string;
}

// Define a type for the DataSourceCatalogueDisplay props
type DataSourceCatalogueDisplayProps = {
  dataSources: DataSourceMetaDeta[];
  commentary: string;
};

// Modified DataSourceCatalogueDisplay component
const DataSourceCatalogueDisplay: React.FC<DataSourceCatalogueDisplayProps> = ({ dataSources, commentary }) => {
  // Organize data sources by category
  // Inside DataSourceCatalogueDisplay component
  const sourcesByCategory = dataSources.reduce((acc: CategoryAccumulator, source) => {
    const { category } = source;
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(source);
    return acc;
  }, {} as CategoryAccumulator);

  return (
    <div className="data-source-catalogue-display">
      <h2>{commentary}</h2>
      {Object.entries(sourcesByCategory).map(([category, sources], index) => (
        <DataSourceCategory
          key={index}
          category={category}
          dataSources={sources}
        />
      ))}
    </div>
  );
};

export default DataSourceCatalogueDisplay;