class ChatService {
    private apiUrl: string;
  
    constructor(apiUrl: string) {
      this.apiUrl = apiUrl;
    }
  
    async sendMessage(message: string): Promise<string> {
      try {
        const response = await fetch(`${this.apiUrl}/ask`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ input: message }),
        });
  
        const data = await response.json();
  
        if (!response.ok) {
          throw new Error(data.error || 'Something went wrong');
        }
  
        return data.output;
      } catch (error) {
        throw error;
      }
    }
  }
  
  export default ChatService;
  