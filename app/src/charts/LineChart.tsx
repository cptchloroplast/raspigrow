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
  
    const yMinValue = d3.min(data, (d) => d.value)
    const yMaxValue = d3.max(data, (d) => d.value)
    const xMinValue = d3.min(data, (d) => d.label)
    const xMaxValue = d3.max(data, (d) => d.label)
    
    const xScale = d3
      .scaleLinear()
      .domain([xMinValue, xMaxValue])
      .range([0, width])
    const yScale = d3
      .scaleLinear()
      .range([height, 0])
      .domain([0, yMaxValue]);
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
      .x((d: any) => xScale(d.label))
      .y((d: any) => yScale(d.value))
      .curve(d3.curveMonotoneX);
    svg
      .append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "#000000")
      .attr("stroke-width", 1)
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
