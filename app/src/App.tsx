import LineChart from "./charts/LineChart"
import useSensors from "./useSensors"

function App() {
  const { chart, current } = useSensors()
  const raw = JSON.stringify(current, null, "\t")
  
  return (
    <div>
      <pre>{raw}</pre>
      {chart.length && <LineChart width={400} height={300} data={chart} />}
    </div>
  )
}

export default App
