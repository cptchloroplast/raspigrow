FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /App
COPY . /App
RUN dotnet restore
RUN dotnet publish -o out

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS release
WORKDIR /App
COPY --from=build /App/out .

FROM release AS migrations
ENTRYPOINT ["dotnet", "Grow.Console.dll"]

FROM release AS worker
ENTRYPOINT ["dotnet", "Grow.Worker.dll"]

FROM release AS api
ENTRYPOINT ["dotnet", "Grow.Api.dll"]