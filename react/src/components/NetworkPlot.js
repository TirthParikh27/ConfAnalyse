import React, { useState, useEffect } from "react";
import { Card, CardContent, Typography } from "@mui/material";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
// import io from "socket.io-client";\

// let endPoint = "http://localhost:5000";
// let socket = io.connect(`${endPoint}`);
export default function NetworkPlot({ data, dataKey, title }) {
  return (
    <Card>
      <Typography variant="h5">{title}</Typography>
      <CardContent>
        <ResponsiveContainer key={Math.random()} width="100%" height={250}>
          <LineChart
            key={Math.random()}
            height={250}
            data={data}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="count" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              key={Math.random()}
              isAnimationActive={false}
              type="monotone"
              dataKey={dataKey}
              stroke="#8884d8"
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
