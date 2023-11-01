class ChatService {
    private apiUrl: string;
  
    constructor(apiUrl: string) {
      this.apiUrl = apiUrl;
    }
  
    async sendMessage(message: string, model: string): Promise<{output: string, estimated_cost: number, data?: any[]}> {
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
  
        return { output: data.output, estimated_cost: data.estimated_cost, data: data.data };
      } catch (error) {
        throw error;
      }
    }
  }
  
  export default ChatService;
  