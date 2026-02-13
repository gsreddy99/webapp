# Runtime image (AMD64)
FROM --platform=linux/amd64 mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80

# Build image (AMD64)
FROM --platform=linux/amd64 mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy only the project file first
COPY EmbeddedServerApp/EmbeddedServerApp.csproj EmbeddedServerApp/
RUN dotnet restore EmbeddedServerApp/EmbeddedServerApp.csproj

# Copy the rest of the project
COPY EmbeddedServerApp/ EmbeddedServerApp/

# Publish
RUN dotnet publish EmbeddedServerApp/EmbeddedServerApp.csproj -c Release -o /app/publish

# Final runtime image
FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
COPY EmbeddedServerApp/public ./public
ENTRYPOINT ["dotnet", "EmbeddedServerApp.dll"]
