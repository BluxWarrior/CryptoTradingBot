import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Label } from "recharts";


const data = [
  { time: 'A', price: 400, MA50: 240, MA200: 100 },
  { time: 'B', price: 600, MA50: 480, MA200: 480 },
  { time: 'C', price: 800, MA50: 360, MA200: 240 },
  { time: 'D', price: 1000, MA50: 800, MA200: 990 },
  { time: 'E', price: 1200, MA50: 540, MA200: 760 },
  { time: 'F', price: 1400, MA50: 960, MA200: 640 },
  { time: 'G', price: 1600, MA50: 780, MA200: 840 },
  { time: 'H', price: 1800, MA50: 620, MA200: 680 },
]

const Chart = ({historicaldata}) => {
  return (
    <LineChart
      width={600}
      height={400}
      data={historicaldata}
      style={{
        marginLeft : "auto",
        marginRight : "auto",
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="time" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="price" stroke="#8884d8" activeDot={{ r: 8 }} />
      <Line type="monotone" dataKey="MA50" stroke="#82ca9d" />
      <Line type="monotone" dataKey="MA200" stroke="#ffc658" />
    </LineChart>
  );
};

export default Chart;
