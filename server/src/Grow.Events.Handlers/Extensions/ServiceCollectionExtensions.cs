using Grow.Sensor;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Okkema.Messages.Extensions;
using Okkema.SQL.Repositories;
namespace Grow.Events.Handlers.Extensions;
public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddEventHandlers(this IServiceCollection services, IConfiguration configuration)
    {
        services
            .AddMqttMessageHandler<SensorReadingV1, SensorReadingV1Handler>(configuration)
            .AddAutoMapper(typeof(MapperProfile))
            .AddSingleton<IRepository<SensorReadingEntity>, SensorReadingRepository>();
        return services;
    }
}