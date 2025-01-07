using Grow.Events;
using Grow.Events.Handlers.Extensions;
using Okkema.Queue.Extensions;
using Okkema.Queue.Producers;
using Okkema.SQL.Extensions;
IConfiguration configuration = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .AddEnvironmentVariables()
    .Build();
IHost host = Host.CreateDefaultBuilder(args)
    .ConfigureServices(services =>
    {
        services
            .AddSQLite(configuration)
            .AddEventHandlers(configuration)
            .AddMqttProducer<SensorReadingV1>(configuration);
    })
    .Build();
// Create random Sensor Reading to simulate client
var services = host.Services;
using var scope = services.CreateScope();
var producer = scope.ServiceProvider.GetRequiredService<IProducer<SensorReadingV1>>();
var random = new Random();
_ = Task.Run(async () => {
    await Task.Delay(5000);
    await producer.WriteAsync(new SensorReadingV1{ 
        Temperature = (float)random.NextDouble(), 
        Humidity = (int)random.NextInt64(),
    });
});
await host.RunAsync();
