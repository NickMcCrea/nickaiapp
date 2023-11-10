// components/GenericChart.tsx
import React from 'react';
import SimpleBarChart, { BarChartData } from './SimpleBarChart';
import SimpleLineChart, { LineChartData } from './SimpleLineChart';
import BasicTable from './BasicTable';

type ChartType = 'bar' | 'line' | 'table';

interface GenericChartProps {
  type: ChartType;
  data: BarChartData[] | LineChartData[];
  metaData: {
    XAxisTitle: string;
    YAxisTitle: string;
    ChartTitle: string;
  };
}

const GenericChart: React.FC<GenericChartProps> = ({ type, data, metaData }) => {
  switch (type) {
    case 'bar':
      return <SimpleBarChart data={data as BarChartData[]} {...metaData} />;
    case 'line':
      return <SimpleLineChart data={data as LineChartData[]} {...metaData} />;
    case 'table':
      return <BasicTable data={data} />;
    default:
      return null;
  }
};

export default GenericChart;
