import { useEffect, useState } from "react"

export type SensorReading = {
  timestamp: string
  topic: string
  event: "message"
  data: {
    temperature: number
    humidity: number
  }
}

export const V1_PATH = "/api/v1/sensor/stream"

const useSensorStream = (length = 60) => {
  const [current, setCurrent] = useState<SensorReading>()
  const [history, setHistory] = useState<SensorReading[]>([])

  useEffect(() => {
    const eventSource = new EventSource(V1_PATH);
    eventSource.addEventListener("message", (event) => {
      const reading: SensorReading = JSON.parse(event.data)
      setCurrent(reading)
      setHistory(history => {
        const temp = [...history, reading]
        if (temp.length > length) temp.shift()
        return temp
      })
    });
    return () => eventSource.close()
  }, [])

  return {
    current,
    history,
  }
}

export default useSensorStream
