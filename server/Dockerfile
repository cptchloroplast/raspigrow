FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /App
COPY . /App
RUN --mount=type=bind,target=. \
    --mount=type=secret,id=NUGET_USERNAME,env=NUGET_USERNAME \
    --mount=type=secret,id=NUGET_PASSWORD,env=NUGET_PASSWORD \
    dotnet restore
RUN dotnet publish -o out

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /App
COPY --from=build /App/out .

FROM runtime AS migrations
ENTRYPOINT ["dotnet", "Grow.Console.dll"]

FROM runtime AS worker
ENTRYPOINT ["dotnet", "Grow.Worker.dll"]

FROM runtime AS api
ENTRYPOINT ["dotnet", "Grow.Api.dll"]