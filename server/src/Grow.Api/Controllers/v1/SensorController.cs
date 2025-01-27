using System.Text.Json;
using AutoMapper;
using Grow.Sensor;
using Microsoft.AspNetCore.Mvc;
using Okkema.Queue.Consumers;
namespace Grow.Api;
/// <summary>
/// Sensor V1 Endpoints
/// </summary>
[ApiController]
[Route("v1/[controller]")]
public class SensorController : ControllerBase
{
    private const string StreamContentType = "text/event-stream";
    private readonly ILogger<SensorController> _logger;
    private readonly IConsumer<Events.SensorReadingV1> _consumer;
    private readonly ITimeSeriesRepository<SensorReadingEntity> _repository;
    private readonly IMapper _mapper;
#pragma warning disable CS1591 // Missing XML comment
    public SensorController(ILogger<SensorController> logger, IConsumer<Events.SensorReadingV1> consumer, IMapper mapper, ITimeSeriesRepository<SensorReadingEntity> repository)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _consumer = consumer ?? throw new ArgumentNullException(nameof(consumer));
        _mapper = mapper ?? throw new ArgumentNullException(nameof(mapper));
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
    }
#pragma warning restore CS1591
    /// <summary>
    /// Stream sensor data
    /// </summary>
    /// <param name="cancellationToken"></param>
    /// <remarks>
    /// Stream sensor data from the API via [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events), published at 1 second intervals.
    /// The data is JSON formatted with the following structure:
    /// ```
    /// {
    ///     "timestamp": date-time,
    ///     "temperature": float,
    ///     "humidity": integer
    /// }
    /// ```
    /// Note on units:
    /// - `timestamp` is ISO 8601 format in UTC
    /// - `temperature` is celcius (C)
    /// - `humidity` is percent relative humidity (%RH)
    /// </remarks>
    /// <returns></returns>
    [HttpGet(nameof(Stream), Name = "Stream Sensor")]
    [Produces(StreamContentType)]
    [ProducesResponseType(StatusCodes.Status200OK)]
    public async Task Stream(CancellationToken cancellationToken)
    {
        Response.ContentType = StreamContentType;
        await _consumer.ReadAsync(async (@event, ct) => {
            var model = _mapper.Map<Models.SensorReadingV1>(@event);
            var json = JsonSerializer.Serialize(model);
            await Response.WriteAsync(json, ct);
            await Response.Body.FlushAsync(ct);
        }, cancellationToken);
    }

    /// <summary>
    /// Returns 
    /// </summary>
    /// <param name="cancellationToken"></param>
    /// <returns></returns>
    [HttpGet(nameof(History), Name = "Sensor History")]
    [Produces("application/json")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    public IEnumerable<Models.SensorReadingV1> History(CancellationToken cancellationToken)
    {
        var entities = _repository.Range(DateTime.UtcNow.AddDays(-1), DateTime.UtcNow);
        var models = _mapper.Map<List<Models.SensorReadingV1>>(entities);
        return models;
    }
}