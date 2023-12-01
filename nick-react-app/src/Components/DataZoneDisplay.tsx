import React from 'react';
import { DataSourceMetaDeta } from './DataSourceMetaDeta';
import {DataSourceCatalogueDisplayProps} from './DataSourceCatalogueDisplayProps';




// Modified DataSourceCatalogueDisplay component
const DataZoneDisplay: React.FC<DataSourceCatalogueDisplayProps> = ({ dataSources, commentary }) => {
 

  //loop through the data sources and display the name
  return(

    <div>
    {dataSources.map((dataSource, index) => (
      <div key={index} className="data-source-card">
        <p>{dataSource.name}</p>
      </div>
    ))}
  </div>

  );
}



export default DataZoneDisplay;