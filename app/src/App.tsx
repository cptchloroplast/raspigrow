import LineChart from "./charts/LineChart"
import useSensors from "./useSensors"

function App() {
  const { chart, current } = useSensors()
  const raw = JSON.stringify(current, null, "\t")
  const stream = JSON.stringify(chart, null, "\t")
  
  return (
    <div>
      <pre>{raw}</pre>
      <LineChart width={400} height={300} data={chart} />
    </div>
  )
}

export default App
