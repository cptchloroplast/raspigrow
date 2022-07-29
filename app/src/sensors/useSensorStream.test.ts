import { test, expect, vi } from "vitest"
import { renderHook } from "@testing-library/react"
import EventSource, { sources } from "eventsourcemock"
import useSensorStream, { V1_PATH } from "./useSensorStream"
import type { SensorReading } from "./useSensorStream"

vi.stubGlobal("EventSource", EventSource)

const createReading = (index: number): SensorReading => {
    const timestamp = new Date()
    timestamp.setSeconds(timestamp.getSeconds() + index)
    return {
        channel: "grow:V1:test",
        event: "message",
        timestamp: timestamp.toISOString(),
        data: {
            temperature: 25,
            humidity: 36,
        }
    }
}

test("useSensorStream", async () => {
    // arrange
    const length = 10
    const readings: SensorReading[] = [...Array(length + 1)].map((_, index) => createReading(index))
    const { result } = renderHook(() => useSensorStream(length))
    const source = sources[V1_PATH]
    // act
    source.emitOpen()
    readings.forEach(x => source.emit("message", { data: JSON.stringify(x) }))
    await new Promise(x => setTimeout(x, 1000)) // wait for changes to flush
    // assert
    expect(result.current).toBeDefined()
    expect(result.current.history.length).toBe(length) // only maintain length of history
    expect(result.current.history.find(x => x.timestamp == readings[0].timestamp)).toBeUndefined() // first reading discarded
    expect(result.current.current).toEqual(readings[length]) // last reading is current
})