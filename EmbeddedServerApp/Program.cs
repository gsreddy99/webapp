using Microsoft.Extensions.FileProviders;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Serve static files from the "public" directory inside the container
app.UseStaticFiles(new StaticFileOptions
{
    FileProvider = new PhysicalFileProvider(
        Path.Combine(Directory.GetCurrentDirectory(), "public")
    ),
    RequestPath = ""
});

// REST API endpoint
app.MapGet("/api/hello", () => "Hello World");

// Calculator API endpoint
app.MapGet("/api/calculate", (double a, double b, string op) =>
{
    double result = op switch
    {
        "add" => EmbeddedServerApp.Models.Calculator.Add(a, b),
        "subtract" => EmbeddedServerApp.Models.Calculator.Subtract(a, b),
        "multiply" => EmbeddedServerApp.Models.Calculator.Multiply(a, b),
        "divide" => EmbeddedServerApp.Models.Calculator.Divide(a, b),
        _ => double.NaN
    };

    return Results.Json(new { result });
});

app.Run();