# Runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80

# Build image
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY EmbeddedServerApp/EmbeddedServerApp.csproj EmbeddedServerApp/
RUN dotnet restore EmbeddedServerApp/EmbeddedServerApp.csproj

COPY EmbeddedServerApp/ EmbeddedServerApp/

RUN dotnet publish EmbeddedServerApp/EmbeddedServerApp.csproj \
    -c Release \
    -o /app/publish \
    -r linux-x64 \
    --self-contained false

# Final image
FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
COPY EmbeddedServerApp/public ./public
ENTRYPOINT ["dotnet", "EmbeddedServerApp.dll"]