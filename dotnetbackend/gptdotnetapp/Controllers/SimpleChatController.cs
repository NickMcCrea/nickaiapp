using Microsoft.AspNetCore.Mvc;
using OpenAI.Interfaces;
using OpenAI.ObjectModels;
using OpenAI.ObjectModels.RequestModels;

namespace gptdotnetapp.Controllers;

[ApiController]
[Route("[controller]")]
public class SimpleChatController : ControllerBase
{
    private readonly IOpenAIService _openAIService;
    private static readonly string[] Summaries = new[]
    {
        "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
    };

    private readonly ILogger<SimpleChatController> _logger;

    public SimpleChatController(ILogger<SimpleChatController> logger, IOpenAIService openAIService)
    {
        _logger = logger;
        _openAIService = openAIService;
    }

    
    [HttpPost]
    public string Ask([FromBody] string query)
    {
        var completionResult = _openAIService.ChatCompletion.CreateCompletion(new ChatCompletionCreateRequest
        {
            Messages = new List<ChatMessage>
                {
                    ChatMessage.FromSystem("You are a helpful assistant."),
                    ChatMessage.FromUser(query)
                },
            MaxTokens = 50,
            Model = Models.Gpt_3_5_Turbo
        });

        completionResult.Wait();

        return completionResult.Result.Choices.First().Message.Content;

      
    }


}
