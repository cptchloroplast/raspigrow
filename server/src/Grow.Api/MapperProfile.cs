using AutoMapper;
using Grow.Sensor;
namespace Grow.Api;
#pragma warning disable CS1591 // Missing XML comment
public class MapperProfile : Profile
{
    public MapperProfile()
    {
        CreateMap<Events.SensorReadingV1, Models.SensorReadingV1>()
            .ForMember(dest => dest.Timestamp, opt => opt.MapFrom(src => src.SystemCreatedDate));
        CreateMap<SensorReadingEntity, Models.SensorReadingV1>();
    }
}
#pragma warning restore CS1591
