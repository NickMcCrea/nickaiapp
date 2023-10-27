using OpenAI.Extensions;
using OpenAI.Interfaces;
using OpenAI.Playground.TestHelpers;



var configBuilder = new ConfigurationBuilder()
    .AddJsonFile("ApiSettings.json");



IConfiguration configuration = configBuilder.Build();




var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddSingleton(_ => configuration);
builder.Services.AddOpenAIService();
var sdk = builder.Services.BuildServiceProvider().GetRequiredService<IOpenAIService>();

await ChatCompletionTestHelper.RunSimpleChatCompletionTest(sdk);


var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();



