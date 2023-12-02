import React, {useState} from 'react';
import { DataSourceMetaDeta } from './DataSourceMetaDeta';
import {DataSourceCatalogueDisplayProps} from './DataSourceCatalogueDisplayProps';
import StorageIcon from '@mui/icons-material/Storage';
import './DataZoneDisplay.css';
import { DataSourceManifest } from './MetaDataDisplay/DataSourceManifest';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';




// Modified DataSourceCatalogueDisplay component
const DataZoneDisplay: React.FC<DataSourceCatalogueDisplayProps> = ({ dataSources, commentary }) => {
 
  const [selectedCard, setSelectedCard] = useState<string | null>(null);

  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event: React.ChangeEvent<{}>, newValue: number) => {
    setActiveTab(newValue);
  };


  //store meta data we get back from the api
  const [metaData, setMetaData] = useState<DataSourceManifest | null>(null);

  const handleCardClick = (dataSource: DataSourceMetaDeta) => {
    setSelectedCard(dataSource.name); // assuming 'name' is unique for each dataSource
    fetchMetaData(dataSource.name);
  };

  const fetchMetaData = async (dataSourceName: string) => {
    const url = `http://127.0.0.1:5001/get_meta_data?data_source_name=${encodeURIComponent(dataSourceName)}`;
    try {
      const response = await fetch(url);
      const data = await response.json();
    
      setMetaData(data);

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

      {metaData && (
        <div className='right-panel-data-source-header'>
          {/* Display the metadata here. Adjust as needed based on the structure of your metadata */}
          <h2>{metaData.displayname || metaData.name}</h2>
          <hr/>
          <h3>Metadata:</h3>
          <p>{metaData.description}</p>
        
 {/* Conditional rendering for optional properties */}
 {metaData.displayname && <p><strong>Display Name:</strong> {metaData.displayname}</p>}
 {metaData.name && <p><strong>Name:</strong> {metaData.name}</p>}
  {metaData.version && <p><strong>Version:</strong> {metaData.version}</p>}
  {metaData.owner && <p><strong>Owner:</strong> {metaData.owner}</p>}
  {metaData.category && <p><strong>Category:</strong> {metaData.category}</p>}
 
 
        </div>
      )}

<Tabs
          value={activeTab}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          centered
          variant='fullWidth'
        >
      
          <Tab label="Fields" />
          <Tab label="Data Sample" />
          <Tab label="Request Access" />
          <Tab label="Data Quality" />
          <Tab label="Data Dictionary" />
          {/* Add more tabs as needed */}
        </Tabs>

        {/* Content of Tab Panels */}
        {activeTab === 0 && (
          <div>
            {/* Content for Tab 1 */}
          </div>
        )}
        {activeTab === 1 && (
          <div>
            {/* Content for Tab 2 */}
          </div>
        )}


    </div>
  </div>

  );
}



export default DataZoneDisplay;