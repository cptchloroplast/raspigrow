import useSensors from "./useSensors"

function App() {
  const data = useSensors()
  const json = JSON.stringify(data, null, "\t")
  
  return (
    <div>
      <pre>{json}</pre>
    </div>
  )
}

export default App
