import SocketClient from "./SocketClient";
import { RestService } from "./RestService";

// Define a type for the possible function call responses
type FunctionCallResponse = {
  name: string;
  arguments: string;
};

// Extend the response type to include all possible properties
type ChatServiceResponse = {
  output: string;
  data?: any[];
  metadata?: any[];
  function_call?: FunctionCallResponse; // This is the new property to handle function call responses
};

export type ProgressData = {
  status: string;
  message: string;
};


class ChatService {
  private apiUrl: string;
  socketClient: SocketClient;
  restService: RestService = new RestService();

  constructor(apiUrl: string) {
    
    this.apiUrl = apiUrl;
    this.socketClient = new SocketClient(apiUrl);

    // Register the endpoints
    this.restService.registerEndpoint('ask', {
      url: `${this.apiUrl}/ask`,
      method: 'POST',
    });
   
  }



  // Call this method to clean up when the service is no longer needed
  cleanup = () => {
    this.socketClient.cleanup();
  };

  // The sendMessage method remains the same as your existing implementation
  async sendMessage(message: string, model: string): Promise<ChatServiceResponse> {
    

    //make JSON object
    const body = {
      input: message,
      model: model
    };

    // Send the message to the server
    const response = await this.restService.makeRequest<ChatServiceResponse>('ask',  body );
  
    return response;

  }

  // Add any additional methods as necessary
}

export default ChatService;
