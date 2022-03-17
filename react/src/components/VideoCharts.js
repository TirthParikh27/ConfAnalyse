import { Grid } from "@mui/material";
import React, { useEffect, useState } from "react";
import NetworkPlot from "./NetworkPlot";

function VideoCharts({ data }) {
  return (
    <div>
      <Grid container spacing={6}>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="videoloss"
            title="Video Packet Loss per second"
          />
        </Grid>

        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="videofps"
            title="Video FPS"
          />
        </Grid>
        {/* <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="videojitter"
            title="Video Jitter per second"
          />
        </Grid> */}
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="videobw"
            title="Video Throughput (Kbps)"
          />
        </Grid>
        <Grid item xs={12}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="videopktRate"
            title="Video Packets per second"
          />
        </Grid>
      </Grid>
    </div>
  );
}

export default VideoCharts;
