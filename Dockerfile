FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS base
WORKDIR /app
EXPOSE 80

FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY EmbeddedServerApp/EmbeddedServerApp.csproj EmbeddedServerApp/
RUN dotnet restore EmbeddedServerApp/EmbeddedServerApp.csproj
COPY . .
WORKDIR /src/EmbeddedServerApp
RUN dotnet publish -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "EmbeddedServerApp.dll"]
