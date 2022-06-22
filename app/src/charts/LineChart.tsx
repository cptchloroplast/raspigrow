import * as d3 from "d3";
import { useEffect } from "react";

type LineChartProps = {
  width: number;
  height: number;
  data: any[];
};

const LineChart = ({ width, height, data }: LineChartProps) => {
  const margin = { top: 50, right: 50, bottom: 50, left: 50 }
  const svg = d3
    .select("#container")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    
  const render = () => {
    svg
      .selectAll("*")
      .remove()
  
    svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`)
  
    const yMinValue = d3.min(data, (d) => d.y)
    const yMaxValue = d3.max(data, (d) => d.y)
    const xMinValue = d3.min(data, (d) => d.x)
    const xMaxValue = d3.max(data, (d) => d.x)
    
    const xDomainStart = xMaxValue < 100 ? 0 : xMaxValue - 100
    const xDomainEnd = xMaxValue < 100 ? 100 : xMaxValue

    const xScale = d3
      .scaleLinear()
      .domain([xDomainStart, xDomainEnd])
      .range([0, width])
    const yScale = d3
      .scaleLinear()
      .range([height, 0])
      .domain([yMinValue - 5, yMaxValue + 5]);
    svg
      .append("g")
      .attr("class", "grid")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(xScale).tickSize(-height));
    svg
      .append("g")
      .attr("class", "grid")
      .call(d3.axisLeft(yScale).tickSize(-width));

    const line = d3
      .line()
      .x((d: any) => xScale(d.x))
      .y((d: any) => yScale(d.y))
      .curve(d3.curveMonotoneX);
    svg
      .append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "red")
      .attr("stroke-width", 2)
      .attr("class", "line")
      .attr("d", line);
  };

  useEffect(() => {
    if (data) {
      render()
    }
  }, [data])

  return <>
    <svg id="container" />
  </>
};

export default LineChart;
