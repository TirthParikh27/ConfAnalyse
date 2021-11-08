import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import { Card, CardContent, Typography } from "@mui/material";
const data = {
  labels: ["1", "2", "3", "4", "5", "6"],
  datasets: [
    {
      label: "# of Votes",
      data: [12, 19, 3, 5, 2, 3],
      fill: false,
      backgroundColor: "rgb(255, 99, 132)",
      borderColor: "rgba(255, 99, 132, 0.2)",
    },
  ],
};

const options = {
  scales: {
    yAxes: [
      {
        ticks: {
          beginAtZero: true,
        },
      },
    ],
  },
};

const NetworkChart = () => {
  const [data, setData] = useState({seq : [] , count : []});
  useEffect(() => {
    // (1) define within effect callback scope
    const fetchData = async () => {
      try {
        const res = await fetch("http://localhost:5000/api/metrics");
        const json = await res.json();
        const newData = data;
        console.log(data);
        newData.count.push(json.count);
        newData.seq.push(json.seq);
        
        setData(newData);
      } catch (error) {
        console.log(error);
      }
    };

    const id = setInterval(() => {
      fetchData(); // <-- (3) invoke in interval callback
    }, 1000);

    fetchData(); // <-- (2) invoke on mount

    return () => clearInterval(id);
  }, []);
  const chartData = {
    labels: data.count.slice(-100),
    datasets: [
      {
        label: "# of Votes",
        data: data.seq.slice(-100),
        fill: false,
        backgroundColor: "rgb(255, 99, 132)",
        borderColor: "rgba(255, 99, 132, 0.2)",
      },
    ],
  };
  console.log(chartData)
  const options = {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
    },
  };
  return (
    <>
      <Line data={chartData} options={options} redraw={true} />
    </>
  );
};

export default NetworkChart;
