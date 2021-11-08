import { Typography } from "@mui/material";
import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";

export default function ApexPlot(props) {
  const arr = () => {
    let dataArray = [];
    for (let i = 0; i < 30; i++) {
      dataArray.push(0);
    }
    return dataArray;
  };
  const [data, updateData] = useState({ seq: arr(), count: arr() });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://localhost:5000/api/metrics");
        const json = await res.json();
        const val = json["seq"];
        const val2 = json["count"];
        let array = [...data["seq"], val];
        let array2 = [...data["count"], val2];
        array.shift();
        array2.shift();
        updateData({ count: array2, seq: array });
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
  const series = [
    {
      name: "seq",
      data: data.seq,
    },
    // {
    //   name: "packetCount",
    //   data: data.count,
    // },
  ];
  const options = {
    chart: {
      height: 300,
      type: "line",
      zoom: {
        enabled: true,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      width: 2,
      curve: "smooth",
    },
    colors: ["#210124"],
    fill: {
      type: "gradient",
      gradient: {
        shadeIntensity: 1,
        inverseColors: true,
        gradientToColors: ["#DB162F"],
        opacityFrom: 1,
        opacityTo: 1,
        type: "vertical",
        stops: [0, 30],
      },
    },
  };
  return (
    <div id="chart">
      <Typography variant="h5" gutterBottom >RTP Sequence Number , Packet Count</Typography>
      <Chart options={options} series={series} type="line" height={350} />
    </div>
  );
}
