# -------------------------
# Runtime image
# -------------------------
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80

# -------------------------
# Build image
# -------------------------
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy project file and restore dependencies
COPY EmbeddedServerApp/EmbeddedServerApp.csproj EmbeddedServerApp/
RUN dotnet restore EmbeddedServerApp/EmbeddedServerApp.csproj

# Copy source
COPY EmbeddedServerApp/ EmbeddedServerApp/

# Build and publish
RUN dotnet publish EmbeddedServerApp/EmbeddedServerApp.csproj \
    -c Release \
    -o /app/publish

# -------------------------
# Final image
# -------------------------
FROM base AS final
WORKDIR /app

COPY --from=build /app/publish .
COPY EmbeddedServerApp/public ./public

ENTRYPOINT ["dotnet", "EmbeddedServerApp.dll"]