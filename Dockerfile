# Base SDK image (multi-arch)
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore dependencies
COPY EmbeddedServerApp/EmbeddedServerApp.csproj EmbeddedServerApp/
RUN dotnet restore EmbeddedServerApp/EmbeddedServerApp.csproj

# Copy full source and publish
COPY EmbeddedServerApp/ EmbeddedServerApp/
RUN dotnet publish EmbeddedServerApp/EmbeddedServerApp.csproj \
    -c Release -o /app/publish

# Runtime image (multi-arch)
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish ./

EXPOSE 80
ENTRYPOINT ["dotnet", "EmbeddedServerApp.dll"]