using Okkema.Messages;
namespace Grow.Events;
public record SensorReadingV1 : MessageBase
{
    public float Temperature { get; set; }
    public int Humidity { get; set; }
}
