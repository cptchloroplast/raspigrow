using Microsoft.Extensions.Logging;
using Okkema.Messages.Handlers;
using Okkema.Queue.Consumers;
using Okkema.Queue.Producers;
namespace Grow.Events.Handlers;
public class SensorReadingV1Handler : MessageHandlerBase<SensorReadingV1>
{
    private readonly IProducer<SensorReadingV1> _producer;
    public SensorReadingV1Handler(
        ILogger<SensorReadingV1Handler> logger,
        IConsumer<SensorReadingV1> consumer,
        IProducer<SensorReadingV1> producer
    ) : base(logger, consumer)
    {
        _producer = producer ?? throw new ArgumentNullException(nameof(producer));
    } 
    public override async Task HandleAsync(SensorReadingV1 @event, CancellationToken cancellationToken = default)
    {
        _logger.LogDebug("Received Sensor Reading V1 with {SystemKey}", @event.SystemKey);
        await Task.Delay(1000);
        var random = new Random();
        await _producer.WriteAsync(new SensorReadingV1{ 
            Temperature = (float)random.NextDouble(), 
            Humidity = (int)random.NextInt64(),
        });
    }
}
