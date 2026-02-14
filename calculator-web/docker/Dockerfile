# ---------- Build stage ----------
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj
COPY src/CalculatorWeb.csproj .

# Restore
RUN dotnet restore CalculatorWeb.csproj

# Copy everything else
COPY src .

# Publish
RUN dotnet publish -c Release -o /publish

# ---------- Runtime stage ----------
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

COPY --from=build /publish .

ENTRYPOINT ["dotnet", "CalculatorWeb.dll"]
