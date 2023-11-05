import * as React from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export interface LineChartData {
  name: string;
  uv: number;
  pv: number;
  amt: number;
}

interface SimpleLineChartProps {
  data: LineChartData[];
}

const SimpleLineChart = ({ data }: SimpleLineChartProps) => (
  <ResponsiveContainer width="100%" height="100%">
    <LineChart data={data}>
      <Line type="monotone" dataKey="total1" stroke="#0D9CD9" />
      <Line type="monotone" dataKey="total2" stroke="#015C94" />
      <Line type="monotone" dataKey="total3" stroke="#94C5EB" />
      <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
      <XAxis dataKey="time" />
      <YAxis/>
      <Tooltip />
    </LineChart>
  </ResponsiveContainer>
);

export default SimpleLineChart;
