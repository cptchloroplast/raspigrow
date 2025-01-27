using Okkema.SQL.Entities;
namespace Grow.Sensor;
public interface ITimeSeriesRepository<T> where T : EntityBase
{
    public IEnumerable<T> Range(DateTime start, DateTime end);
}