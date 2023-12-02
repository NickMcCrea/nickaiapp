import React, {useState} from 'react';
import { DataSourceMetaDeta } from './DataSourceMetaDeta';
import {DataSourceCatalogueDisplayProps} from './DataSourceCatalogueDisplayProps';
import StorageIcon from '@mui/icons-material/Storage';
import './DataZoneDisplay.css';




// Modified DataSourceCatalogueDisplay component
const DataZoneDisplay: React.FC<DataSourceCatalogueDisplayProps> = ({ dataSources, commentary }) => {
 
  const [selectedCard, setSelectedCard] = useState<string | null>(null);

  const handleCardClick = (dataSource: DataSourceMetaDeta) => {
    setSelectedCard(dataSource.name); // assuming 'name' is unique for each dataSource
  };

  //loop through the data sources and display the name
  return(

    <div className="data-zone-display">
    <div className="left-panel">
    {dataSources.map((dataSource, index) => (

          <div 
          className={`data-zone-card ${selectedCard === dataSource.name ? 'selected' : ''}`}
          onClick={() => handleCardClick(dataSource)}
          key={index}
          >
     
        <div className='data-zone-card-icon'><StorageIcon className="icon" style={{ fontSize: 80 }} /> </div>
      
      <div className='data-zone-card-text'>
        <h3>{dataSource.name}</h3>
        <p>{dataSource.description}</p>
        <p>{dataSource.category}</p>
      </div>
      
      </div>

    ))}
  </div>
  <div className="right-panel">
    </div>
  </div>

  );
}



export default DataZoneDisplay;