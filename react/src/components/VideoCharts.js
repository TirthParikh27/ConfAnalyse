import { Grid } from "@mui/material";
import React, { useEffect, useState } from "react";
import NetworkPlot from "./NetworkPlot";
import UxPlot from "./UxPlot";

function VideoCharts({ data }) {
  return (
    <div>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <UxPlot type="video" uxData={data.slice(-100)} />
        </Grid>
        <Grid item xs={6}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="videoloss"
            title="Video Packet Loss per second"
          />
        </Grid>

        <Grid item xs={6}>
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
        <Grid item xs={6}>
          <NetworkPlot
            data={data.slice(-100)}
            dataKey="videobw"
            title="Video Throughput (Kbps)"
          />
        </Grid>
        <Grid item xs={6}>
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
