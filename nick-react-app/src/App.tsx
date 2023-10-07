import React, { useState,useEffect } from 'react';
import ChatService from './Services/ChatService';
import ChatHistory, { Message } from './Components//ChatHistory'; // Adjust the import path as needed
import InputWithSendButton from './Components/InputWithSendButton'; // Adjust the import path as needed
import DollarAmount, { DollarAmountProvider } from './Components/DollarAmount';
import Header from './Components/Header';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);

  const chatService = new ChatService("http://localhost:5001");
  

  const handleSendMessage = async (content: string) => {
    // Append user's message to ChatHistory
    setMessages([...messages, { type: 'text', content, timestamp: new Date() }]);
    
    try {
      // Get the reply from the server
      const reply = await chatService.sendMessage(content);
      
      // Append the server's reply to ChatHistory
      setMessages(prevMessages => [...prevMessages, { type: 'text', content: reply, timestamp: new Date() }]);
    } catch (error) {
      console.error('Failed to send message:', error);
    }

  };

  return (
    <div className="App">
      <DollarAmountProvider>
      <Header />
      <ChatHistory messages={messages} />
      <InputWithSendButton onSubmit={handleSendMessage} />
      </DollarAmountProvider>
     
    </div>
  );
}

export default App;
