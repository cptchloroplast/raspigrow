import { useEffect, useState } from "react"

const useSensors = () => {
  const [data, setData] = useState<MessageEvent<any>>()

  useEffect(() => {
    const eventSource = new EventSource("/api/stream");
    eventSource.addEventListener("message", (event) => {
      setData(JSON.parse(event.data))
    }); 
  })

  return data
}

export default useSensors
