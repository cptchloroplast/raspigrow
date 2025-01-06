IConfiguration configuration = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .AddEnvironmentVariables()
    .Build();

IHost host = Host.CreateDefaultBuilder(args)
    // .ConfigureServices(services =>
    // {
    // })
    .Build();
var services = host.Services;
await host.RunAsync();
