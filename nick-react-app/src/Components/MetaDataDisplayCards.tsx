import React from 'react';
import DataSet from './DataSet';
import './DataSetCollection.css'; // Path to your CSS file

// TypeScript interface for the DataSetCollection props
interface DataSetCollectionProps {
  dataSets: any[]; // Array of data source manifest objects
}

const MetaDataCollectionDisplay: React.FC<DataSetCollectionProps> = ({ dataSets }) => {
  return (
    <div className="data-set-collection">
      {dataSets.map((dataSourceManifest, index) => (
        <DataSet key={index} dataSourceManifest={dataSourceManifest} />
      ))}
    </div>
  );
};

export default MetaDataCollectionDisplay;
