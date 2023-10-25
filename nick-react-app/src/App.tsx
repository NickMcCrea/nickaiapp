import React, { useState,useEffect } from 'react';
import { Resizable, ResizableBox } from 'react-resizable'; // New import
import ChatService from './Services/ChatService';
import ChatHistory, { Message } from './Components//ChatHistory'; // Adjust the import path as needed
import InputWithSendButton from './Components/InputWithSendButton'; // Adjust the import path as needed
import Header from './Components/Header';
import AIChatBox from './Components/AIChatBox'; // New import
import { Grid } from '@mui/material'; // New import
import "react-resizable/css/styles.css"; // New import for styling
import './App.css';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [estimatedCost, setEstimatedCost] = useState<string>(""); // New state variable
  const [selectedModel, setSelectedModel] = useState('GPT3.5'); // New state variable for selected model

  const handleModelChange = (model: string) => { // New function to handle model change
    setSelectedModel(model);
    //console print
    console.log(model);
  };

  const [width, setWidth] = useState(600);

  const onResize = (event: any, { size }: any) => {
    setWidth(size.width);
  };


  const handleSendMessage = async (content: string) => {
    // Append user's message to ChatHistory

    
    const chatService = new ChatService("http://localhost:5001");

    setMessages([...messages, { type: 'text', content, timestamp: new Date(), sender: 'You' }]);
    
    try {
      // Get the reply from the server
      const reply = await chatService.sendMessage(content, selectedModel);

      //print selected model
      console.log(selectedModel);

      const estimatedCost = reply.estimated_cost; // Extract this from the reply
      
      //print this to the console
      console.log(estimatedCost);
      setEstimatedCost(reply.estimated_cost.toString()); // Update estimatedCost state
     
      
      // Append the server's reply to ChatHistory
      setMessages(prevMessages => [...prevMessages, { type: 'text', content: reply.output, timestamp: new Date(), sender: 'Assistant' }]);
    } catch (error) {
      console.error('Failed to send message:', error);
    }

  };

  return (
    <div className="App">
     
      <Header estimatedCost={estimatedCost} selectedModel={selectedModel} onModelChange={handleModelChange}/>
      <Grid container spacing={3}>
        <Grid item>
          {/* Wrap AIChatBox inside ResizableBox component */}
          <ResizableBox 
            width={width} 
            height={300} 
            onResize={onResize} 
            minConstraints={[100, 300]} 
            maxConstraints={[800, 300]}
            handle={<span className="react-resizable-handle react-resizable-handle-e"></span>}
          >
            <div style={{ width, height: 300 }}>
              <AIChatBox messages={messages} handleSendMessage={handleSendMessage}/>
            </div>
          </ResizableBox>
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
