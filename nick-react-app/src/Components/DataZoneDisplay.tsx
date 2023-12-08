import React, { useState } from 'react';
import { DataSourceMetaDeta } from './DataSourceMetaDeta';
import { DataSourceCatalogueDisplayProps } from './DataSourceCatalogueDisplayProps';
import { styled } from '@mui/system';
import './DataZoneDisplay.css';
import { DataSourceManifest } from './MetaDataDisplay/DataSourceManifest';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import BasicTable from './Charts/BasicTable';
import BasicDataGridAgGrid from './Charts/BasicAgGrid';
import MiniAskAI from './MiniAskAI';
import StorageIcon from '@mui/icons-material/Storage';
import ListIcon from '@mui/icons-material/List';
import FolderCopyIcon from '@mui/icons-material/FolderCopy';
import BarChartIcon from '@mui/icons-material/BarChart';
import TableChartIcon from '@mui/icons-material/TableChart';
import AddchartIcon  from '@mui/icons-material/Addchart';
import PieChartIcon from '@mui/icons-material/PieChart';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import SportsBasketballIcon from '@mui/icons-material/SportsBasketball';


import Icon from '@mui/material/Icon';
import powerBiImage from './power-bi.png';






// Modified DataSourceCatalogueDisplay component
const DataZoneDisplay: React.FC<DataSourceCatalogueDisplayProps> = ({ dataSources, onPowerBiClick, chatService : ChatService }) => {


  const [selectedCard, setSelectedCard] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);
  //store meta data we get back from the api
  const [metaData, setMetaData] = useState<DataSourceManifest | null>(null);
  //store meta data we get back from the api
  const [sampleData, setSampleData] = useState<any>(null);
  const [fields, setFields] = useState<any>(null);

  //set the chat service
  const chatService = ChatService;

  const renderIcon = (metadata: any) => {
    let fontsize = 60;
    // Example condition, replace with your actual logic
    if (metadata.category.includes('Reference')) {
      return <FolderCopyIcon className="icon" style={{ fontSize: fontsize, color: '#94C5EB' }} />;
    }
    if (metadata.category.includes('Regulatory')) {
      return <BarChartIcon className="icon" style={{ fontSize: fontsize, color: '#94C5EB' }} />;
    }
    if (metadata.category.includes('Capital')) {
      return <AddchartIcon className="icon" style={{ fontSize: fontsize, color: '#0D9CD9' }} />;
    }
    if (metadata.category.includes('Sports')) {
      return <SportsBasketballIcon className="icon" style={{ fontSize: fontsize, color: '#C9E0F5' }} />;
    }
    if (metadata.category.includes('Balances')) {
      return <PieChartIcon className="icon" style={{ fontSize: fontsize, color: '#95A3AB' }} />;
    }
    else {
      return <StorageIcon className="icon" style={{ fontSize: fontsize, color: '#94C5EB' }} />;
    }
  };
  

  // 
const renderPowerBiIcon = (metadata: any, onClickHandler : (powerBiValue: string) => void) => {
  // Example condition, replace with your actual logic
  if (metadata.powerbi) {
   
    return ( 
      <div className='data-zone-card-icon-two' onClick={() => onClickHandler(metadata.powerbi)}>
    <img src={powerBiImage} alt="Power BI Icon" style={{scale: '90%'}}/>
    </div>
    );
   
  }
};

interface SegmentColorMap {
  [key: string]: string;
}

const renderCategory = (category: string) => {
  let segments = category.split('>');
  let color = '#000000';

  segments = segments.map((segment) => segment.trim());

  // A map of strings to colour
  // Can add more segments as needed
  // Can add more colors as needed
  const segmentToColorMap: SegmentColorMap = {
    'Finance': '#015C94',
    'Capital': '#A1A5D9',
    'RWA': '#95A3AB',
    'Balances': '#01C5C4',
    'Reference': '#015C94',
    'Counterparty': '#0D9CD9',
    'Product': '#0D9CD9',
    'FINREP': '#0D9CD9',
    'GL Balances': '#015C94',
    'Sports': '#015C94',
    'Regulatory': '#015C94',
  };

  // How do I call this segmentToColorMap with the segment name?
  // How do I get the color from the map?

  return (
    <p>
      {segments.map((segment, index) => (
        // Switch statement to change the color of the segment
        // Based on the segment name
        // Can add more segments as needed
        // Can add more colors as needed
        <span key={index} style={{ color: segmentToColorMap[segment] || color }}>
          {index < segments.length-1 ? segment + ' > ' : segment}
        </span>
      ))}
    </p>
  );
};



  const handleTabChange = (event: React.ChangeEvent<{}>, newValue: number) => {
    setActiveTab(newValue);

    //if tab 2 is clicked, fetch the data
    if (newValue === 1) {
      fetchSampleData(selectedCard!);
    }

  };


  //fetch some rows of data from the api, hit get_sample_data endpoint
  const fetchSampleData = async (dataSourceName: string) => {
  
    try {
      
      const data = await chatService.restService.makeRequest<any>('get_sample_data', undefined, { "data_source_name" : dataSourceName });

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


    //clear fields and sample data
    setFields(null);
    setSampleData(null);

  };



  const fetchMetaData = async (dataSourceName: string) => {
    try {

      const queryParams =  { "data_source_name" : dataSourceName };
      console.log(queryParams);
      const data = await chatService.restService.makeRequest<any>('get_meta_data', undefined, queryParams);
     

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

            <div className='data-zone-card-icon'>
              {renderIcon(dataSource)}
            </div>
            <div className='data-zone-card-text'>
              <h3>{dataSource.name}</h3>
              <p>{dataSource.description}</p>
             {renderCategory(dataSource.category)}
            </div>

          
             {renderPowerBiIcon(dataSource, onPowerBiClick)}
            
          
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


            >
              <Tab label="Fields" />
              <Tab label="Data Sample" />
              <Tab label="Request Access" />
              <Tab label="Data Quality" />
              <Tab label="Data Dictionary" />
              <Tab label="Ask" />
              {/* Add more tabs as needed */}
            </Tabs>

            {/* Content of Tab Panels */}
            {activeTab === 0 && (
              <div style={{ overflow: 'auto', margin: '10px' }}>
                {
                  fields && (<BasicTable data={fields} />)
                }
              </div>
            )}
            {activeTab === 1 && (
              <div style={{ overflow: 'auto', margin: '10px' }}>
                {sampleData && (<BasicTable data={sampleData} />)}
              </div>
            )}

            {activeTab === 2 && (
              <div style={{ overflow: 'auto', margin: '10px' }}>
                <p>Request Access</p>
              </div>
            )}

            {activeTab === 3 && (
              <div style={{ overflow: 'auto', margin: '10px' }}>
                <p>Data Quality</p>
              </div>
            )}

            {activeTab === 4 && (
              <div style={{ overflow: 'auto', margin: '10px' }}>
                <p>Data Dictionary</p>
              </div>
            )}

            {activeTab === 5 && (
              <div style={{ margin: '10px', overflow: 'auto' }}>
                <MiniAskAI dataSourceName={selectedCard} chatService={chatService} />
              </div>
            )}

            {/* Add more tabs as needed */}
          </>
        )}
      </div>
    </div>

  );
}



export default DataZoneDisplay;