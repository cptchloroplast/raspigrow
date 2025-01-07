using Okkema.SQL.Entities;
namespace Grow.Sensor;
public record SensorReadingEntity : EntityBase
{
    public DateTime Timestamp { get; set; }
    public float Temperature { get; set; }
    public int Humidity { get; set; }
}