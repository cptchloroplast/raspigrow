import { useEffect, useState } from "react"

type SensorHistory = {
  id: number
  timestamp: string
  temperature: number
  humidity: number
}

const useSensorHistory = (start?: Date, end?: Date) => {
  const [data, setData] = useState<SensorHistory[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(false)

  useEffect(() => {
    (async () => {
      setError(false)
      setLoading(true)
      const response = await fetch("/api/v1/sensor/history")
      setLoading(false)
      if (!response.ok) {
        setError(true)
        const message = await response.text()
        console.error(message)
      } else {
        const json = await response.json()
        setData(json)
      }
    })()
  }, [])

  return {
    data,
    loading,
    error,
  }
}

export default useSensorHistory
