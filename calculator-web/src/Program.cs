using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.FileProviders;
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;
using System.Net.Http;
using System.Text.Json;
using System.IO;

var builder = WebApplication.CreateBuilder(args);

// Add Swagger services
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// 1. Read API key from Key Vault at startup
var kvUrl = builder.Configuration["KEYVAULT_URL"];
var secretClient = new SecretClient(new Uri(kvUrl), new DefaultAzureCredential());
var apiKey = (await secretClient.GetSecretAsync("WebAppApiKey")).Value.Value;

// 2. Register HttpClient and attach API key header
builder.Services.AddHttpClient("webapi", client =>
{
    // IMPORTANT: Use your new WebAPI public IP
    client.BaseAddress = new Uri("http://172.212.180.93");

    // Add API key header for every request
    client.DefaultRequestHeaders.Add("x-api-key", apiKey);
});

var app = builder.Build();

// Enable Swagger UI
app.UseSwagger();
app.UseSwaggerUI();

// Serve static files from "public" folder
app.UseStaticFiles(new StaticFileOptions
{
    FileProvider = new PhysicalFileProvider(
        Path.Combine(Directory.GetCurrentDirectory(), "public")
    ),
    RequestPath = ""
});

// Simple hello endpoint
app.MapGet("/api/hello", () => "Hello World");

// Calculator endpoint (calls webapi)
app.MapGet("/api/calculate", async (
    double a,
    double b,
    string op,
    IHttpClientFactory httpClientFactory) =>
{
    var client = httpClientFactory.CreateClient("webapi");

    var url = $"/api/calc?a={a}&b={b}&op={op}";
    var response = await client.GetAsync(url);

    if (!response.IsSuccessStatusCode)
    {
        return Results.BadRequest(new
        {
            error = "webapi returned an error",
            status = (int)response.StatusCode
        });
    }

    var json = await response.Content.ReadAsStringAsync();
    var result = JsonSerializer.Deserialize<JsonElement>(json);

    return Results.Json(result);
});

app.Run();
