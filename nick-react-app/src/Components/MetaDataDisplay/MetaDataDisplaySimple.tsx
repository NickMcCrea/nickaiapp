import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledTableContainer = styled(TableContainer)(({ theme }) => ({
  marginBottom: theme.spacing(4),
  '&:last-child': {
    marginBottom: 0,
  },
}));

const DataSetTitle = styled(Typography)(({ theme }) => ({
  margin: theme.spacing(2, 0),
  fontWeight: 'bold',
}));

interface Field {
  fieldName: string;
  fieldDescription: string;
  fieldType: string;
}

interface DataSet {
  name: string;
  description: string;
  fields: Field[];
}

interface DataSetCollectionProps {
  dataSets: DataSet[];
}

const MetaDataDisplaySimple: React.FC<DataSetCollectionProps> = ({ dataSets }) => {
  return (
    <div>
      {dataSets.map((dataSet: DataSet, index: number) => (
        <Paper key={index} elevation={3} style={{ marginBottom: '24px', marginTop: '24px' }}>
          <StyledTableContainer>
            <DataSetTitle variant="h6">{dataSet.name}</DataSetTitle>
            <Typography variant="body2" color="textSecondary">{dataSet.description}</Typography>
            <Table sx={{ minWidth: 650 }} size="small" aria-label={`${dataSet.name} fields`}>
              <TableHead>
                <TableRow>
                  <TableCell>Field Name</TableCell>
                  <TableCell align="right">Type</TableCell>
                  <TableCell align="right">Description</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {dataSet.fields.map((field: Field, fieldIndex: number) => (
                  <TableRow
                    key={fieldIndex}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                  >
                    <TableCell component="th" scope="row">
                      {field.fieldName}
                    </TableCell>
                    <TableCell align="right">{field.fieldType}</TableCell>
                    <TableCell align="right">{field.fieldDescription}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </StyledTableContainer>
        </Paper>
      ))}
    </div>
  );
};

export default MetaDataDisplaySimple;
