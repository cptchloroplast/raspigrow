using AutoMapper;
using Grow.Sensor;
using Microsoft.Extensions.Logging;
using Okkema.Messages.Handlers;
using Okkema.Queue.Consumers;
using Okkema.Queue.Producers;
using Okkema.SQL.Repositories;
namespace Grow.Events.Handlers;
public class SensorReadingV1Handler : MessageHandlerBase<SensorReadingV1>
{
    private readonly IMapper _mapper;
    private readonly IRepository<SensorReadingEntity> _repository;
    private readonly IProducer<SensorReadingV1> _producer;
    public SensorReadingV1Handler(
        ILogger<SensorReadingV1Handler> logger,
        IConsumer<SensorReadingV1> consumer,
        IMapper mapper,
        IRepository<SensorReadingEntity> repository,
        IProducer<SensorReadingV1> producer
    ) : base(logger, consumer)
    {
        _mapper = mapper ?? throw new ArgumentNullException(nameof(mapper));
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
        _producer = producer ?? throw new ArgumentNullException(nameof(producer));
    } 
    public override async Task HandleAsync(SensorReadingV1 @event, CancellationToken cancellationToken = default)
    {
        _logger.LogDebug("Received Sensor Reading V1: Temperature {Temperature}, Humidity {Humidity}", @event.Temperature, @event.Humidity);
        var entity = _mapper.Map<SensorReadingEntity>(@event);
        _repository.Create(entity);
        await Task.Delay(1000);
        var random = new Random();
        await _producer.WriteAsync(new SensorReadingV1{ 
            Temperature = (float)random.NextDouble(), 
            Humidity = (int)random.NextInt64(),
        });
    }
}
