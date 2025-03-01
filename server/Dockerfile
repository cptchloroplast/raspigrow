FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG TARGETARCH
WORKDIR /App
COPY . /App
RUN --mount=type=secret,id=nuget_username,env=NUGET_USERNAME \
    --mount=type=secret,id=nuget_password,env=NUGET_PASSWORD \
    dotnet restore -a $TARGETARCH
RUN dotnet publish -o out -a $TARGETARCH

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /App
COPY --from=build /App/out .

FROM runtime AS migrations
ENTRYPOINT ["dotnet", "Grow.Console.dll"]

FROM runtime AS worker
ENTRYPOINT ["dotnet", "Grow.Worker.dll"]

FROM runtime AS api
ENTRYPOINT ["dotnet", "Grow.Api.dll"]