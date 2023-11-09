import * as React from 'react';
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer, Label } from 'recharts';

export interface BarChartData {
    XAxis: string;
    Total: number;
}

interface SimpleBarChartProps {
  data: BarChartData[];
  XAxisTitle: string;
  YAxisTitle: string;
  ChartTitle: string;
}

const SimpleBarChart = ({ data, XAxisTitle, YAxisTitle, ChartTitle }: SimpleBarChartProps) => (
  <ResponsiveContainer width="100%" height="100%">
    <BarChart data={data}>
      <Bar dataKey="Total" fill="#0D9CD9" />
      
      <XAxis dataKey="X-Axis">
        <Label value={XAxisTitle} offset={-8} position="insideBottom" />
      </XAxis>
      <YAxis dataKey="Total"> 
        <Label value={YAxisTitle} offset={0} angle={-90} position='insideLeft' style={{ textAnchor: 'middle' }} />
      </YAxis>
      <Tooltip />
      {/* Custom Label for the Chart Title */}
      <text x={'50%'} y={2} textAnchor="middle" dominantBaseline="hanging" style={{ fontSize: '20px' }}>
        {ChartTitle}
      </text>
    </BarChart>

  </ResponsiveContainer>
);

export default SimpleBarChart;
