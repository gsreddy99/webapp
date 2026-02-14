using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.FileProviders;
using EmbeddedServerApp.Models;

namespace EmbeddedServerApp
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // Register services if needed
            ConfigureServices(builder.Services);

            var app = builder.Build();

            // Configure middleware
            Configure(app);

            // Run the application
            app.Run();
        }

        private static void ConfigureServices(IServiceCollection services)
        {
            // Add services here if needed (e.g., controllers, DI)
        }

        private static void Configure(WebApplication app)
        {
            // Serve static files from "public" folder
            app.UseStaticFiles(new StaticFileOptions
            {
                FileProvider = new PhysicalFileProvider(
                    Path.Combine(Directory.GetCurrentDirectory(), "public")
                ),
                RequestPath = ""
            });

            // Map API endpoints
            MapEndpoints(app);
        }

        private static void MapEndpoints(WebApplication app)
        {
            // Simple hello endpoint
            app.MapGet("/api/hello", Hello);

            // Calculator endpoint
            app.MapGet("/api/calculate", Calculate);
        }

        // Methods for endpoints
        private static string Hello() => "Hello World";

        private static IResult Calculate(double a, double b, string op)
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
        }
    }
}
