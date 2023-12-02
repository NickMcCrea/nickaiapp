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
    fetchMetaData(dataSource.name);
  };

  const fetchMetaData = async (dataSourceName: string) => {
    const url = `http://127.0.0.1:5001/get_meta_data?data_source_name=${encodeURIComponent(dataSourceName)}`;
    try {
      const response = await fetch(url);
      const data = await response.json();
      console.log(data); // Handle the response data as needed
    } catch (error) {
      console.error('Error fetching meta data:', error);
    }
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