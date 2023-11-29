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
    api.sizeColumnsToFit();
  };

  // Generate column definitions
  const columns = Object.keys(data[0]).map(key => ({
    headerName: key,
    field: key,
    sortable: true,
    filter: true
  }));

  return (
    <div className="ag-theme-alpine" style={{ height: 400, width: '100%' }}>
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
