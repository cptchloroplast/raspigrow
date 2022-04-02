function App() {
  const evtSource = new EventSource("http://localhost:8000/stream");
  evtSource.addEventListener("message", function(event) {
      // Logic to handle status updates
      console.log(event.data)
  });  
  
  return (
    <div>Grow</div>
  )
}

export default App
