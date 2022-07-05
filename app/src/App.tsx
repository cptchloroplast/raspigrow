import LineChart from "./charts/LineChart"
import useSensors from "./useSensors"

function App() {
  const { history, current } = useSensors()
  const raw = JSON.stringify(current, null, "\t")
  const temperature = history.map(x => ({ x: new Date(x.timestamp), y: x.data.temperature }))
  const humidity = history.map(x => ({ x: new Date(x.timestamp), y: x.data.humidity }))
  return (
    <div>
      <pre>{raw}</pre>
      {!!history.length && <LineChart data={temperature} />}
      {!!history.length && <LineChart data={humidity} color="blue" />}
    </div>
  )
}

export default App
