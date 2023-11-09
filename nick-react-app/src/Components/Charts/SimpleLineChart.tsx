import * as React from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer,Label } from 'recharts';

export interface LineChartData {
  name: string;
  uv: number;
  pv: number;
  amt: number;
}

interface SimpleLineChartProps {
  data: LineChartData[];
  XAxisTitle: string;
  YAxisTitle: string;
  ChartTitle: string;
}

const SimpleLineChart = ({ data, XAxisTitle, YAxisTitle, ChartTitle }: SimpleLineChartProps) => (
  <ResponsiveContainer width="100%" height="100%">
    <LineChart data={data} margin={{ top: 20, right: 20, left: 20, bottom: 30 }}>
      <Line type="monotone" dataKey="total1" stroke="#0D9CD9" />
      <Line type="monotone" dataKey="total2" stroke="#015C94" />
      <Line type="monotone" dataKey="total3" stroke="#94C5EB" />
      <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
      <XAxis dataKey="time"> 
      <Label value={XAxisTitle} offset={-15} position="insideBottom" />
      </XAxis>
      
      <YAxis>
      <Label value={YAxisTitle} offset={-10} angle={-90} position='insideLeft' style={{ textAnchor: 'middle' }} />
      </YAxis>
      <Tooltip />
      <text x={'50%'} y={2} textAnchor="middle" dominantBaseline="hanging" style={{ fontSize: '20px' }}>
        {ChartTitle}
      </text>
    </LineChart>
  </ResponsiveContainer>
);

export default SimpleLineChart;
