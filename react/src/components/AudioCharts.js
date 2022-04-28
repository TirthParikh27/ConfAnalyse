import { Grid } from "@mui/material";
import React, { useEffect, useState } from "react";
import NetworkPlot from "./NetworkPlot";
import UxPlot from "./UxPlot";

function AudioCharts({ data }) {

  return (
    <div>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <UxPlot type="audio" uxData={data.slice(-100)} />
        </Grid>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="loss"
            title="Audio Packet Loss / second (%)"
            height={200}
          />
        </Grid>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="jitter"
            title="Audio Jitter (ms)"
            height={200}
          />
        </Grid>
        <Grid item xs={6}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="newJitter"
            title="Audio Packet Inter-Arrival Jitter (ms)"
            height={220}
          />
        </Grid>
        <Grid item xs={6}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="delay"
            title="Audio Receiving Delay (sec)"
            height={220}
          />
        </Grid>
        <Grid item xs={6}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="bw"
            title="Audio Throughput (Kbps)"
            height={220}
          />
        </Grid>
        <Grid item xs={6}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="pktRate"
            title="Audio Packets per second"
            height={220}
          />
        </Grid>
      </Grid>
    </div>
  );
}

export default AudioCharts;
