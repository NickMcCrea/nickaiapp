import * as React from 'react';
import { DataGridPremium, GridColDef } from '@mui/x-data-grid-premium';
import Paper from '@mui/material/Paper';



interface BasicDataGridPremiumProps {
  data: any[];
}

const BasicDataGridPremium: React.FC<BasicDataGridPremiumProps> = ({ data }) => {
  const rows = data.map((row, index) => ({ id: index, ...row }));
  const columns: GridColDef[] = Object.keys(data[0]).map((key) => ({
    field: key,
    headerName: key,
    width: 150,
  }));

  return (
    <Paper style={{ height: 400, width: '100%' }}>
      <DataGridPremium
        rows={rows}
        columns={columns}
        checkboxSelection
      />
    </Paper>
  );
};

export default BasicDataGridPremium;
