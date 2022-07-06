import { useEffect, useState } from "react"

type SensorReading = {
  timestamp: Date
  channel: string
  event: "message"
  data: {
    temperature: number
    humidity: number
  }
}


const useSensorStream = (length = 30) => {
  const [current, setCurrent] = useState<SensorReading>()
  const [history, setHistory] = useState<SensorReading[]>([])

  useEffect(() => {
    const eventSource = new EventSource("/api/v1/sensor/stream");
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
