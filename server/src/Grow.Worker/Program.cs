using Grow.Events;
using Grow.Events.Handlers;
using Okkema.Messages.Extensions;
using Okkema.Queue.Extensions;
using Okkema.Queue.Producers;
IConfiguration configuration = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .AddEnvironmentVariables()
    .Build();
IHost host = Host.CreateDefaultBuilder(args)
    .ConfigureServices(services =>
    {
        services.AddMessageHandler<SensorReadingV1, SensorReadingV1Handler>();
        services.AddChannelProducer<SensorReadingV1>();
    })
    .Build();
var services = host.Services;
using var scope = services.CreateScope();
var producer = scope.ServiceProvider.GetRequiredService<IProducer<SensorReadingV1>>();
var random = new Random();
await producer.WriteAsync(new SensorReadingV1{ 
    Temperature = (float)random.NextDouble(), 
    Humidity = (int)random.NextInt64(),
});
await host.RunAsync();
