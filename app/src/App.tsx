import { useEffect, useState } from "react";
import LineChart from "./charts/LineChart"
import useSensors from "./useSensors"

function App() {
  const raw = useSensors()
  const json = JSON.stringify(raw, null, "\t")
  const [data, setData] = useState()

  useEffect(() => {
    setData(data => [...data, raw])
  }, [raw])

  // const chartData = [];
  //   for (let i = 0; i < 20; i++) {
  //     const value = Math.floor(Math.random() * i + 3);
  //     chartData.push({
  //       label: i,
  //       value,
  //       tooltipContent: `<b>x: </b>${i}<br><b>y: </b>${value}`
  //     });
  //   }
  
  return (
    <div>
      <pre>{json}</pre>
      <LineChart width={400} height={300} data={chartData} />
    </div>
  )
}

export default App
