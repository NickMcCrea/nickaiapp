import SocketClient from "./SocketClient";

// Define a type for the possible function call responses
type FunctionCallResponse = {
  name: string;
  arguments: string;
};

// Extend the response type to include all possible properties
type ChatServiceResponse = {
  output: string;
  data?: any[];
  metaData?: any[];
  function_call?: FunctionCallResponse; // This is the new property to handle function call responses
};

export type ProgressData = {
  status: string;
  message: string;
};


class ChatService {
  private apiUrl: string;
  socketClient: SocketClient;

  constructor(apiUrl: string) {
    
    this.apiUrl = apiUrl;
    this.socketClient = new SocketClient(apiUrl);

   // Connect to the socket when the service is instantiated
  }



  // Call this method to clean up when the service is no longer needed
  cleanup = () => {
    this.socketClient.cleanup();
  };

  // The sendMessage method remains the same as your existing implementation
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

      const chatResponse: ChatServiceResponse = {
        output: data.output,
        data: data.data,
        metaData: data.metadata,
        function_call: data.function_call,
      };

      return chatResponse;
    } catch (error) {
      throw error;
    }
  }

  // Add any additional methods as necessary
}

export default ChatService;
