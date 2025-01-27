using System.Reflection;
using Grow.Api;
using Grow.Events;
using Grow.Sensor;
using Microsoft.OpenApi.Models;
using Okkema.Queue.Extensions;
using Okkema.SQL.Extensions;
IConfiguration configuration = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .AddEnvironmentVariables()
    .Build();
var builder = WebApplication.CreateBuilder(args);
builder.Services
    .AddSQLite(configuration)
    .AddMqttConsumer<SensorReadingV1>(configuration)
    .AddSingleton<ITimeSeriesRepository<SensorReadingEntity>, SensorReadingRepository>()
    .AddAutoMapper(typeof(MapperProfile))
    .AddSwaggerGen(options =>
    {
        options.SwaggerDoc("v1", new OpenApiInfo
        {
            Version = "development",
            Title = "Grow",
            Description = "Greenhouse Automation Software",
            Contact = new OpenApiContact
            {
                Name = "Okkema Labs",
                Url = new Uri("https://okkema.org")
            },
            License = new OpenApiLicense
            {
                Name = "MIT",
                Url = new Uri("https://github.com/okkema/grow/blob/main/LICENSE")
            }
        });

        var xmlFilename = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
        options.IncludeXmlComments(Path.Combine(AppContext.BaseDirectory, xmlFilename));
    })
    .AddControllers();
var app = builder.Build();
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(options => 
    {
        options.SwaggerEndpoint("/swagger/v1/swagger.json", "v1");
        options.RoutePrefix = string.Empty;
    });
}
app.UseAuthorization();
app.MapControllers();
app.Run();
