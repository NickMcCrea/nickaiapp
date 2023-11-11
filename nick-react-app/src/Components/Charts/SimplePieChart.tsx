import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

export interface PieChartData {
  Name: string;
  Total: number;
}

interface SimplePieChartProps {
  data: PieChartData[];
  ChartTitle: string;
  colors?: string[];
}

const COLORS = ['#0D9CD9', '#015C94', '#94C5EB', '#C9E0F5', '#95A3AB', '#BFCAD9', '#D9E2EC', '#EAF0F5', '#F5F8FA'];

const SimplePieChart = ({ data, ChartTitle, colors = COLORS }: SimplePieChartProps) => (
  <ResponsiveContainer width="100%" height="100%">
    <PieChart>
      <Pie 
        data={data} 
        cx="50%" 
        cy="50%" 
        labelLine={false}
        label={({ Name, Total }) => `${Name}: ${Total}`}
        outerRadius={200} 
        fill="#8884d8"
        dataKey="Total"
      >
        {
          data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
          ))
        }
      </Pie>
      <Tooltip />
     
      {/* Custom Label for the Chart Title */}
      <text x={'50%'} y={20} textAnchor="middle" dominantBaseline="hanging" style={{ fontSize: '20px' }}>
        {ChartTitle}
      </text>
    </PieChart>
  </ResponsiveContainer>
);

export default SimplePieChart;
