import { Grid } from "@mui/material";
import React, { useEffect, useState } from "react";
import NetworkPlot from "./NetworkPlot";

function ScreenShareCharts({ data }) {

  return (
    <div>
      <Grid container spacing={6}>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="screenloss"
            title="SCreen Sharing Packet Loss per second"
          />
        </Grid>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="screenbw"
            title="Screen Sharing Throughput (Kbps)"
          />
        </Grid>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="screenpktRate"
            title="Screen Sharing Packets per second"
          />
        </Grid>
      </Grid>
    </div>
  );
}

export default ScreenShareCharts;

