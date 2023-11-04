// Define a type for the possible function call responses
type FunctionCallResponse = {
  name: string;
  arguments: string;
};

// Extend the response type to include all possible properties
type ChatServiceResponse = {
  output: string;
  estimated_cost: number;
  data?: any[];
  metaData?: any[];
  function_call?: FunctionCallResponse; // This is the new property to handle function call responses
};

class ChatService {
  private apiUrl: string;

  constructor(apiUrl: string) {
    this.apiUrl = apiUrl;
  }

  // Update the method signature to return the extended type
  async sendMessage(message: string, model: string): Promise<ChatServiceResponse> {
    try {
      const response = await fetch(`${this.apiUrl}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ input: message, model }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
      }

      // Construct the response with the new function_call property
      const chatResponse: ChatServiceResponse = {
        output: data.output,
        estimated_cost: data.estimated_cost,
        data: data.data,
        metaData: data.metadata,
        function_call: data.function_call // Handle function call responses
      };

      return chatResponse;
    } catch (error) {
      throw error;
    }
  }
}

export default ChatService;
