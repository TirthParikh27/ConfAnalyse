import { Grid } from "@mui/material";
import React, { useEffect, useState } from "react";
import NetworkPlot from "./NetworkPlot";

function AudioCharts({ data }) {

  return (
    <div>
      <Grid container spacing={6}>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="loss"
            title="Audio Packet Loss per second"
          />
        </Grid>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="jitter"
            title="Audio Jitter per second"
          />
        </Grid>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="newJitter"
            title="Audio Packet Inter-Arrival Jitter"
          />
        </Grid>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="delay"
            title="Audio Receiving Delay"
          />
        </Grid>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="bw"
            title="Audio Throughput (Kbps)"
          />
        </Grid>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="pktRate"
            title="Audio Packets per second"
          />
        </Grid>
      </Grid>
    </div>
  );
}

export default AudioCharts;
