# ---------- Build stage ----------
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore
COPY EmbeddedServerApp/EmbeddedServerApp.csproj EmbeddedServerApp/
RUN dotnet restore EmbeddedServerApp/EmbeddedServerApp.csproj

# Copy source code
COPY EmbeddedServerApp/ EmbeddedServerApp/

# Ensure public folder is copied explicitly
COPY EmbeddedServerApp/public EmbeddedServerApp/public

WORKDIR /src/EmbeddedServerApp

# Publish (includes public/)
RUN dotnet publish -c Release -o /publish --no-restore

# ---------- Runtime stage ----------
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

# Copy published output
COPY --from=build /publish .

EXPOSE 80
ENV ASPNETCORE_URLS=http://+:80

ENTRYPOINT ["dotnet", "EmbeddedServerApp.dll"]
