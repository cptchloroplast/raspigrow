namespace Grow.Api.Models;
/// <summary>
/// Sensor Reading V1
/// </summary>
public record SensorReadingV1
{
    /// <summary>
    /// Timestamp when the reading occurred in ISO 8601 formatted UTC
    /// </summary>
    public DateTime Timestamp { get; set; }
    /// <summary>
    /// Environmental temperature in celcius (C)
    /// </summary>
    public float Temperature { get; set; }
    /// <summary>
    /// Environmental humidity in precent relative humidity (%RH)
    /// </summary>
    public int Humidity { get; set; }
}