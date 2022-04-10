import { useEffect } from "react"

const useSensors = () => {
  useEffect(() => {
    const eventSource = new EventSource("/api/stream");
    eventSource.addEventListener("message", function(event) {
      // Logic to handle status updates
      console.log(event.data)
    }); 
  })
}

export default useSensors
