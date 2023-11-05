import * as React from 'react';
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export interface BarChartData {
    XAxis: string;
    Total: number;
}

interface SimpleBarChartProps {
  data: BarChartData[];
}

const SimpleBarChart = ({ data }: SimpleBarChartProps) => (
  <ResponsiveContainer width="100%" height="100%">
    <BarChart data={data}>
      <Bar dataKey="Total" fill="#0D9CD9" />
      <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
      <XAxis dataKey="X-Axis" />
      <YAxis dataKey="Total"/>
      <Tooltip />
    </BarChart>
  </ResponsiveContainer>
);

export default SimpleBarChart;
