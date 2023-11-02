import React from 'react';
import './FieldCard.css'; // Path to your CSS file

// Define a type for the FieldCard props
type FieldCardProps = {
  fieldName: string;
  fieldDescription: string;
  fieldType: 'STRING' | 'FLOAT'; // Extend this union type as needed for other field types
};

// Define a mapping from field types to colors
const fieldTypeColors: { [key: string]: string } = {
  STRING: '#007bff',
  FLOAT: '#28a745',
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
