import io, { Socket } from 'socket.io-client';
import { EventEmitter } from 'events';

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

type ProgressData = {
  status: string;
  message: string;
};


class ChatService  extends EventEmitter{
  private apiUrl: string;
  private socket!: Socket;

  constructor(apiUrl: string) {
    super();
    this.apiUrl = apiUrl;
    this.connectSocket(); // Connect to the socket when the service is instantiated
  }

  private connectSocket = () => {
    // Initialize the socket connection
    this.socket = io(this.apiUrl);

    // Listen for events
    this.socket.on('progress', this.handleProgress);
    
    // Add other event listeners as needed
  };

  private handleProgress = (progressData: any) => {
    // Assuming progressData is an object with a 'status' and 'message' property
    
    this.emit('progress', progressData);
    // Handle progress data
  };
  // Method to send a message via WebSocket, if needed
  sendSocketMessage = (event: string, message: any) => {
    this.socket.emit(event, message);
  };

  // Call this method to clean up when the service is no longer needed
  cleanup = () => {
    this.socket.off('progress', this.handleProgress);
    this.socket.disconnect();
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
