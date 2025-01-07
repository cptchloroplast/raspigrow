using AutoMapper;
using Grow.Sensor;
namespace Grow.Events.Handlers;
public class MapperProfile : Profile
{
    public MapperProfile()
    {
        CreateMap<SensorReadingV1, SensorReadingEntity>()
            .ForMember(dest => dest.Timestamp, opt => opt.MapFrom(src => src.SystemCreatedDate));
    }
}