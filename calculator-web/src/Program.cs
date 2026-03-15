using Microsoft.Extensions.FileProviders;
using System.IO;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Make signin.html the default page
var defaultFilesOptions = new DefaultFilesOptions();
defaultFilesOptions.DefaultFileNames.Clear();
defaultFilesOptions.DefaultFileNames.Add("signin.html");

// Correct static file path: src/public
var publicPath = Path.Combine(builder.Environment.ContentRootPath, "public");
Console.WriteLine("Serving static files from: " + publicPath);

app.UseDefaultFiles(defaultFilesOptions);
app.UseStaticFiles(new StaticFileOptions
{
    FileProvider = new PhysicalFileProvider(publicPath),
    RequestPath = ""
});

app.Run();
