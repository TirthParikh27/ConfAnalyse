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
  ComposedChart,
  Area,
} from "recharts";

function getUxData(type, uxData) {
  return uxData.map((point, index) => {
    if (type === "audio") {
      return { [point["audioUx"]]: 1, count: point["count"] }
    } else if (type === "video") {
      return { [point["videoUx"]]: 1, count: point["count"] }
    } else return { count: point["count"] }
  })
}


export default function UxPlot({ type, uxData }) {
  return (
    <Card>
      <Typography variant="h6">{type.charAt(0).toUpperCase() + type.slice(1)} User Experience</Typography>
      <CardContent>
        <ResponsiveContainer key={Math.random()} width="100%" height={100}>
          <ComposedChart
            key={Math.random()}
            height={100}
            data={getUxData(type, uxData)}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="count" hide={true} />
            <Legend />
            <Area
              isAnimationActive={false}
              key={Math.random()}
              type="stepAfter"
              dataKey="high"
              name="High"
              fill={"#27c24c"}
              fillOpacity={0.75}
              stroke={0}
            />
            <Area
              isAnimationActive={false}
              key={Math.random()}
              type="stepAfter"
              dataKey="medium"
              name="Medium"
              fill={"#ff902b"}
              fillOpacity={0.75}
              stroke={0}
            />
            <Area
              isAnimationActive={false}
              key={Math.random()}
              type="stepAfter"
              dataKey="low"
              name="Low"
              fill={"#f05050"}
              fillOpacity={0.75}
              stroke={0}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}