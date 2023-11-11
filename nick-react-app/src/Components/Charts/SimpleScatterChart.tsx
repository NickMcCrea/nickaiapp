import React from 'react';
import { ScatterChart, Scatter, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer, Label, TooltipProps } from 'recharts';

export interface ScatterChartData {
  X: number;
  Y: number;
  Z: string; // Name of the element
}



interface SimpleScatterChartProps {
    data: ScatterChartData[];
    XAxisTitle: string;
    YAxisTitle: string;
    ChartTitle: string;
  }
  
  // Update TooltipProps to include your specific data type
  const renderTooltipContent = (props: TooltipProps<number, string>) => {
    const { payload } = props;
  
    if (!payload || payload.length === 0) {
      return null;
    }
  
    // Assuming your payload structure matches your data
    const data = payload[0].payload;
  
    return (
      <div style={{ backgroundColor: 'white', padding: '5px', border: '1px solid #ccc' }}>
        <p>X: {data.X}</p>
        <p>Y: {data.Y}</p>
        <p>Name: {data.Z}</p>
      </div>
    );
  };

const SimpleScatterChart = ({ data, XAxisTitle, YAxisTitle, ChartTitle }: SimpleScatterChartProps) => (
  <ResponsiveContainer width="100%" height="100%">
    <ScatterChart margin={{ top: 20, right: 20, left: 20, bottom: 30 }}>
      <CartesianGrid />
      <XAxis type="number" dataKey="X" name="X-Axis">
        <Label value={XAxisTitle} offset={-15} position="insideBottom" />
      </XAxis>
      <YAxis type="number" dataKey="Y" name="Y-Axis">
        <Label value={YAxisTitle} offset={20} angle={-90} position='insideLeft' style={{ textAnchor: 'middle' }} />
      </YAxis>
      <Tooltip cursor={{ strokeDasharray: '3 3' }} content={renderTooltipContent} />
      <Scatter name={ChartTitle} data={data} fill="#0D9CD9" />
      {/* Custom Label for the Chart Title */}
      <text x={'50%'} y={20} textAnchor="middle" dominantBaseline="hanging" style={{ fontSize: '20px' }}>
        {ChartTitle}
      </text>
    </ScatterChart>
  </ResponsiveContainer>
);

export default SimpleScatterChart;
