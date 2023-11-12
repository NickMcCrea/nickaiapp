import React from 'react';
import './FieldCard.css'; // Path to your CSS file

// Define a type for the FieldCard props
type FieldCardProps = {
  fieldName: string;
  fieldDescription: string;
  fieldType: 'STRING' | 'FLOAT' | 'INTEGER' | 'DATE' | 'BOOLEAN'; // Extend this union type as needed for other field types
};

// Define a mapping from field types to colors
const fieldTypeColors: { [key: string]: string } = {
  STRING: '#1D73B2',
  FLOAT: '#7FABC7',
  INTEGER: '#3E828C',
  DATE: '#145A8D',
  BOOLEAN: '#2E6E8E',
  // Add more types and corresponding colors as needed
};

const FieldCard: React.FC<FieldCardProps> = ({ fieldName, fieldDescription, fieldType }) => {
  return (
    <div className="field-card">
      <h4>{fieldName}</h4>
      <p>{fieldDescription}</p>
      <span className="field-type" style={{ backgroundColor: fieldTypeColors[fieldType] }}>
        {fieldType}
      </span>
    </div>
  );
};

export default FieldCard;
