import React, { useState } from 'react';
import ChatHistory, { Message } from './Components//ChatHistory'; // Adjust the import path as needed
import InputWithSendButton from './Components/InputWithSendButton'; // Adjust the import path as needed
import DollarAmount, { DollarAmountProvider } from './Components/DollarAmount';
import Header from './Components/Header';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSendMessage = (content: string) => {
    setMessages([...messages, { type: 'text', content, timestamp: new Date() }]);
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
