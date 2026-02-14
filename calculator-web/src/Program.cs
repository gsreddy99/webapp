using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.FileProviders;
using CalculatorWeb.Models;
using System.IO;

var builder = WebApplication.CreateBuilder(args);

// Add Swagger services
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

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

// Calculator endpoint
app.MapGet("/api/calculate", (double a, double b, string op) =>
{
    double result = op switch
    {
        "add" => Calculator.Add(a, b),
        "subtract" => Calculator.Subtract(a, b),
        "multiply" => Calculator.Multiply(a, b),
        "divide" => Calculator.Divide(a, b),
        _ => double.NaN
    };

    return Results.Json(new { result });
});

app.Run();
