import * as d3 from "d3"
import { useEffect, useState } from "react"
import { v4 as uuid } from "uuid"

type LineChartProps = {
  width?: number;
  height?: number;
  data: any[];
  color?: "red" | "blue" | "green"
  xDomain?: Date[]
  yDomain?: number[]
};

const LineChart = ({ width = 400, height = 300, data = [], color = "red", xDomain, yDomain }: LineChartProps) => {
  const [id] = useState(`container-${uuid()}`)

  const clear = () => {
    d3.select(`#${id}`)
      .selectAll("*")
      .remove()
  }

  const render = () => {
    const margin = { top: 50, right: 50, bottom: 50, left: 50 }

    const xScale = d3.scaleTime()
      .range([0, width])
      .domain(xDomain ?? [d3.min(data, (d) => d.x), d3.max(data, (d) => d.x)])

    const yScale = d3.scaleLinear()
      .range([height, 0])
      .domain(yDomain ?? [d3.min(data, (d) => d.y), d3.max(data, (d) => d.y)])

    const line = d3.line()
      .x((d: any) => xScale(d.x))
      .y((d: any) => yScale(d.y))
      .curve(d3.curveLinear)

    const svg = d3.select(`#${id}`)
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`)
    svg
      .append("g")
      .attr("class", "grid")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(xScale).tickSize(-height))
    svg  
      .append("g")
      .attr("class", "grid")
      .call(d3.axisLeft(yScale).tickSize(-width))
    svg  
      .append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", color)
      .attr("stroke-width", 2)
      .attr("class", "line")
      .attr("d", line);
  }

  useEffect(() => {
    if (data) {
      clear()
      render()
    }
  }, [data])

  return <>
    <svg id={id} />
  </>
};

export default LineChart;
