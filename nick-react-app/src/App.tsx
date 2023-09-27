import React, { useState } from 'react';
import ChatHistory, { Message } from './Components//ChatHistory'; // Adjust the import path as needed
import InputWithSendButton from './Components/InputWithSendButton'; // Adjust the import path as needed
import DollarAmount from './Components/DollarAmount';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSendMessage = (content: string) => {
    setMessages([...messages, { type: 'text', content, timestamp: new Date() }]);
  };

  return (
    <div className="App">
      <ChatHistory messages={messages} />
      <InputWithSendButton onSubmit={handleSendMessage} />
      <DollarAmount amount={124.56} />
    </div>
  );
}

export default App;
