import React, { useState } from 'react';
import { DataSourceMetaDeta } from './DataSourceMetaDeta';
import { DataSourceCatalogueDisplayProps } from './DataSourceCatalogueDisplayProps';
import StorageIcon from '@mui/icons-material/Storage';
import './DataZoneDisplay.css';
import { DataSourceManifest } from './MetaDataDisplay/DataSourceManifest';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import BasicTable from './Charts/BasicTable';
import BasicDataGridAgGrid from './Charts/BasicAgGrid';




// Modified DataSourceCatalogueDisplay component
const DataZoneDisplay: React.FC<DataSourceCatalogueDisplayProps> = ({ dataSources, commentary }) => {

  const [selectedCard, setSelectedCard] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);

  //store meta data we get back from the api
  const [metaData, setMetaData] = useState<DataSourceManifest | null>(null);
  
  //store meta data we get back from the api
  const [sampleData, setSampleData] = useState<any>(null);

  const[fields, setFields] = useState<any>(null);



  const handleTabChange = (event: React.ChangeEvent<{}>, newValue: number) => {
    setActiveTab(newValue);

    //if tab 2 is clicked, fetch the data
    if (newValue === 1) {
      fetchSampleData(selectedCard!);
    }
  };


  //fetch some rows of data from the api, hit get_sample_data endpoint
   const fetchSampleData = async (dataSourceName: string) => {
    const url = `http://127.0.0.1:5001/get_sample_data?data_source_name=${encodeURIComponent(dataSourceName)}`;
    try {
      const response = await fetch(url);
      const data = await response.json();

      console.log('sample data');
      console.log(data);
      setSampleData(data);

    } catch (error) {
      console.error('Error fetching meta data:', error);
    }

   }


  const handleCardClick = (dataSource: DataSourceMetaDeta) => {
    setSelectedCard(dataSource.name); // assuming 'name' is unique for each dataSource
    fetchMetaData(dataSource.name);
    setActiveTab(-1);
   
  };

 

  const fetchMetaData = async (dataSourceName: string) => {
    const url = `http://127.0.0.1:5001/get_meta_data?data_source_name=${encodeURIComponent(dataSourceName)}`;
    try {
      const response = await fetch(url);
      const data = await response.json();

      
      setMetaData(data);

      //we want a JSON object that has the field names as keys and the values as the values
      //so we need to do some transformation
      console.log('fields');
      console.log(data.fields);

      
      //declare an object array with 3 keys - field_name, field_type, field_description
      let fields: any[] = [];

      //make the keys
      data.fields.forEach((field: any) => {
        fields.push({
          field_name: field.fieldName,
          field_type: field.fieldType,
          field_description: field.fieldDescription
        });
      });

      
      setFields(fields);

    } catch (error) {
      console.error('Error fetching meta data:', error);
    }
  };


  //loop through the data sources and display the name
  return (

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
            <hr />
            <h3>Metadata:</h3>
            <p>{metaData.description}</p>

      <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'flex-start' }}>
      <div style={{ marginRight: '30px', color: '#015C94' }}> {/* Adjust marginRight for spacing */}
      {metaData.displayname && <p><strong>Display Name:</strong></p>}
        {metaData.name && <p><strong>Name:</strong></p>}
        {metaData.version && <p><strong>Version:</strong></p>}
        {metaData.owner && <p><strong>Owner:</strong></p>}
        {metaData.category && <p><strong>Category:</strong></p>}
      </div>
      <div>
        {metaData.displayname && <p>{metaData.displayname}</p>}
        {metaData.name && <p>{metaData.name}</p>}
        {metaData.version && <p>{metaData.version}</p>}
        {metaData.owner && <p>{metaData.owner}</p>}
        {metaData.category && <p>{metaData.category}</p>}
      </div>
    </div>


          </div>
        )}
    {selectedCard && ( // Conditional rendering based on whether a card is selected
        <>
          <Tabs
            value={activeTab}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            centered
            variant='fullWidth'
            style={{ overflow: 'auto'}}
          
          >
            <Tab label="Fields"  />
            <Tab label="Data Sample" />
            <Tab label="Request Access" />
            <Tab label="Data Quality" />
            <Tab label="Data Dictionary" />
            <Tab label="Ask" />
            {/* Add more tabs as needed */}
          </Tabs>

          {/* Content of Tab Panels */}
          {activeTab === 0 && (
            <div  style= {{overflow: 'auto', margin: '10px'}}>
           {
              fields && ( <BasicTable data={fields}/> )
           }
            </div>
          )}
          {activeTab === 1 && (
            <div  style= {{overflow: 'auto', margin: '10px' }}>
              {sampleData &&(   <BasicTable data={sampleData} />) }
            </div>
          )}
        </>
      )}
      </div>
    </div>

  );
}



export default DataZoneDisplay;