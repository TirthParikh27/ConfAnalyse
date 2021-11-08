import { Grid } from "@mui/material";
import React, { useEffect, useState } from "react";
import NetworkPlot from "./NetworkPlot";

function AudioCharts() {
  const [data, updateData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://localhost:5000/api/metrics");
        const json = await res.json();
        updateData([...data, json]);
      } catch (error) {
        console.log(error);
      }
    };
    const interval = setInterval(() => {
      fetchData();
    }, 1000);
    return () => {
      window.clearInterval(interval);
    };
  }, [data]);
  return (
    <div>
      <Grid container spacing={6}>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="loss"
            title="Packet Loss per second"
          />
        </Grid>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="jitter"
            title="Jitter per second"
          />
        </Grid>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="bw"
            title="Throughput (Kbps)"
          />
        </Grid>
      </Grid>
    </div>
  );
}

export default AudioCharts;
