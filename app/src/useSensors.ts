import { useEffect, useState } from "react"

type SensorData = {
  timestamp: Date
  event: "message"
  data: {
    type: "message"
    pattern?: string
    channel: string
    data: {
      temperature: number
      humidity: number
    }
  }
}

type SensorChart = {
  x: Date
  y: number
}

const useSensors = () => {
  const [current, setCurrent] = useState<SensorData>()
  const [chart, setChart] = useState<SensorChart[]>([])

  useEffect(() => {
    const eventSource = new EventSource("/api/v1/stream/");
    eventSource.addEventListener("message", (event) => {
      const raw: SensorData = JSON.parse(event.data)
      setCurrent(raw)
      setChart(chart => [...chart, {
        x: new Date(raw.timestamp),
        y: raw.data.data.temperature,
      }])
    });
  })

  return {
    current,
    chart,
  }
}

export default useSensors
