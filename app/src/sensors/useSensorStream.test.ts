import { test, expect, vi } from "vitest"
import { renderHook } from "@testing-library/react"
import { EventSource } from "mocksse"
import { useSensorStream } from "."

vi.stubGlobal("EventSource", EventSource)

test("useSensorStream", async () => {
    const { result } = renderHook(() => useSensorStream())
    expect(result.current).toBeDefined()
})