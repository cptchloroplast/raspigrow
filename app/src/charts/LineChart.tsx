import * as d3 from "d3";
import { useEffect } from "react";

type LineChartProps = {
  width: number;
  height: number;
  data: any[];
};

const LineChart = ({ width, height, data }: LineChartProps) => {
  const clear = () => {
    d3.select("#container")
      .selectAll("*")
      .remove()
  }

  const render = () => {
    const margin = { top: 50, right: 50, bottom: 50, left: 50 }

    const yMinValue = d3.min(data, (d) => d.y)
    const yMaxValue = d3.max(data, (d) => d.y)
    const xMinValue: Date = d3.min(data, (d) => d.x)
    const xMaxValue: Date = d3.max(data, (d) => d.x)
    
    const xDomainMax = new Date(xMinValue.getTime() + 60 * 1000)
    const xDomainMin = new Date(xMaxValue.getTime() - 60 * 1000)
    const xDomainStart = xMaxValue < xDomainMax ? xMinValue : xDomainMin
    const xDomainEnd = xMinValue > xDomainMin ? xDomainMax : xMaxValue

    const xScale = d3.scaleTime()
      .range([0, width])
      .domain([xDomainStart, xDomainEnd])

    const yScale = d3.scaleLinear()
      .range([height, 0])
      .domain([yMinValue - 5, yMaxValue + 5])

    const line = d3.line()
      .x((d: any) => xScale(d.x))
      .y((d: any) => yScale(d.y))
      .curve(d3.curveLinear)

    const svg = d3.select("#container")
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
      .attr("stroke", "red")
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
    <svg id="container" />
  </>
};

export default LineChart;
