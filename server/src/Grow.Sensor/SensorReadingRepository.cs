using System.Data;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Okkema.SQL.Extensions;
using Okkema.SQL.Factories;
using Okkema.SQL.Options;
using Okkema.SQL.Repositories;
namespace Grow.Sensor;
public class SensorReadingRepository : RepositoryBase<SensorReadingEntity>
{
    public SensorReadingRepository(
        ILogger<SensorReadingRepository> logger,
        IDbConnectionFactory factory,
        IOptionsMonitor<DbConnectionOptions> options
    ) : base(logger, factory, options) { }
    private const string CREATE =
        @"INSERT INTO SensorReading (
            Timestamp,
            Temperature,
            Humidity,
            SystemKey,
            SystemCreatedDate,
            SystemModifiedDate
        )
        VALUES (
            @Timestamp,
            @Temperature,
            @Humidity,
            @SystemKey,
            @SystemCreatedDate,
            @SystemModifiedDate
        );";
    public override int Create(SensorReadingEntity entity) =>
        UseConnection((IDbConnection connection) =>
            connection.ExecuteCommand(CREATE, entity));
    public override int Delete(Guid key)
    {
        throw new NotImplementedException();
    }

    public override SensorReadingEntity? Read(Guid key)
    {
        throw new NotImplementedException();
    }

    public override int Update(SensorReadingEntity entity)
    {
        throw new NotImplementedException();
    }
}
