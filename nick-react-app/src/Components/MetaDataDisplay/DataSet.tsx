import React from 'react';
import FieldCard from './FieldCard';
import './DataSet.css'; // Path to your CSS file
import { DataSourceManifest } from './DataSourceManifest';

// TypeScript interfaces for the JSON structure
export interface Field {
  fieldName: string;
  fieldDescription: string;
  fieldType: string; // You may want to use a union type or enum if you have a fixed set of field types
}

// Props for the DataSet component
type DataSetProps = {
  dataSourceManifest: DataSourceManifest; // Assuming you pass the entire manifest as a prop
};

const DataSet: React.FC<DataSetProps> = ({ dataSourceManifest }) => {
  return (
    <div className="dataset">
      <h2>{dataSourceManifest.name}</h2>
      <p>{dataSourceManifest.description}</p>
      <div className="field-cards-container">
        {dataSourceManifest.fields.map((field, index) => (
          <FieldCard
            key={index} // Ideally, use a unique id for the key if available
            fieldName={field.fieldName}
            fieldDescription={field.fieldDescription}
            fieldType={field.fieldType as 'STRING' | 'FLOAT'} // Cast to the union type, add additional types as needed
          />
        ))}
      </div>
    </div>
  );
};

export default DataSet;
