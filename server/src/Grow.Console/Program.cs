using FluentMigrator.Runner;
using Grow.Migrations;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Okkema.SQL.Extensions;
using System.Reflection;

var configuration = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .AddEnvironmentVariables()
    .Build();

var serviceProvider = new ServiceCollection()
    .AddSQLiteMigrationRunner(configuration, new Assembly[] { 
        typeof(AddSensorReadingTable).Assembly, 
    })
    .BuildServiceProvider();

using var scope = serviceProvider.CreateScope();
var runner = scope.ServiceProvider.GetRequiredService<IMigrationRunner>();
try
{
    runner.MigrateUp();
}
catch (Exception exception)
{
    Console.WriteLine(exception);
}
    