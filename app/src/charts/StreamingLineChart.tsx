import * as d3 from "d3"
import LineChart from "./LineChart"

type StreamingLineChartProps = {
  data: any[]
  color?: "red" | "blue" | "green"
}

const StreamingLineChart = ({ data, color = "red" }: StreamingLineChartProps) => {
  const yMinValue = d3.min(data, (d) => d.y)
  const yMaxValue = d3.max(data, (d) => d.y)
  const xMinValue: Date = d3.min(data, (d) => d.x)
  const xMaxValue: Date = d3.max(data, (d) => d.x)
  
  const xDomainMax = new Date(xMinValue.getTime() + 60 * 1000)
  const xDomainMin = new Date(xMaxValue.getTime() - 60 * 1000)
  const xDomainStart = xMaxValue < xDomainMax ? xMinValue : xDomainMin
  const xDomainEnd = xMinValue > xDomainMin ? xDomainMax : xMaxValue

  return <LineChart 
    data={data} 
    xDomain={[xDomainStart, xDomainEnd]} 
    yDomain={[yMinValue - 5, yMaxValue + 5]}
    color={color}
  />
}

export default StreamingLineChart
