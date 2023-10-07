import React, { useState,useEffect } from 'react';
import ChatService from './Services/ChatService';
import ChatHistory, { Message } from './Components//ChatHistory'; // Adjust the import path as needed
import InputWithSendButton from './Components/InputWithSendButton'; // Adjust the import path as needed
import Header from './Components/Header';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [estimatedCost, setEstimatedCost] = useState<string>(""); // New state variable


  const chatService = new ChatService("http://localhost:5001");



  const handleSendMessage = async (content: string) => {
    // Append user's message to ChatHistory
    setMessages([...messages, { type: 'text', content, timestamp: new Date() }]);
    
    try {
      // Get the reply from the server
      const reply = await chatService.sendMessage(content);

      const estimatedCost = reply.estimated_cost; // Extract this from the reply
      
      //print this to the console
      console.log(estimatedCost);
      setEstimatedCost(reply.estimated_cost.toString()); // Update estimatedCost state
     
      
      // Append the server's reply to ChatHistory
      setMessages(prevMessages => [...prevMessages, { type: 'text', content: reply.output, timestamp: new Date() }]);
    } catch (error) {
      console.error('Failed to send message:', error);
    }

  };

  return (
    <div className="App">
     
      <Header estimatedCost={estimatedCost}/>
      <ChatHistory messages={messages} />
      <InputWithSendButton onSubmit={handleSendMessage} />
     
    </div>
  );
}

export default App;
