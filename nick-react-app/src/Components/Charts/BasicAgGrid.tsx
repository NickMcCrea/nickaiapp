import React from 'react';
import { AgGridReact } from 'ag-grid-react';
import { GridReadyEvent } from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';


interface BasicDataGridAgGridProps {
  data: any[];
}

const BasicDataGridAgGrid: React.FC<BasicDataGridAgGridProps> = ({ data }) => {
  const onGridReady = (params: GridReadyEvent) => {
    const api = params.api;
   
  };

  // Generate column definitions
  const columns = Object.keys(data[0]).map(key => ({
    headerName: key,
    field: key,
    sortable: true,
    filter: true,
    

  }));

  return (
    <div className="ag-theme-alpine" style={{ height: '100%', width: '100%', justifyContent: 'left', textAlign: 'left' }}>
      <AgGridReact 
        onGridReady={onGridReady}
        rowData={data}
        columnDefs={columns}
        rowSelection="multiple"
        
      />
    </div>
  );
};

export default BasicDataGridAgGrid;
