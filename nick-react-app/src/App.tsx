import React, { useState, useEffect } from 'react';
import { ResizableBox } from 'react-resizable';
import ChatService from './Services/ChatService';
import ChatHistory, { Message } from './Components/ChatHistory';
import InputWithSendButton from './Components/InputWithSendButton';
import Header from './Components/Header';
import AIChatBox from './Components/AIChatBox';
import { Grid } from '@mui/material';
import "react-resizable/css/styles.css";
import './App.css';
import BasicTable from './Components/BasicTable';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [estimatedCost, setEstimatedCost] = useState<string>("");
  const [selectedModel, setSelectedModel] = useState('GPT3.5');
  const [tableData, setTableData] = useState<any[]>([]);
  const [width, setWidth] = useState(600); // Default width for the resizable panel
  const [rightPanelWidth, setRightPanelWidth] = useState(window.innerWidth - width); // Width for the right panel

  // This effect adjusts the right panel width when the left panel resizes or the window resizes
  useEffect(() => {
    const updateRightPanelWidth = () => {
      setRightPanelWidth(window.innerWidth - width);
    };

    window.addEventListener('resize', updateRightPanelWidth);

    return () => {
      window.removeEventListener('resize', updateRightPanelWidth);
    };
  }, [width]);

  const onResize = (event: any, { size }: any) => {
    setWidth(size.width);
  };

  const handleModelChange = (model: string) => {
    setSelectedModel(model);
    console.log(model);
  };

  const handleSendMessage = async (content: string) => {
    const chatService = new ChatService("http://localhost:5001");

    setMessages([...messages, { type: 'text', content, timestamp: new Date(), sender: 'You' }]);

    try {
      const reply = await chatService.sendMessage(content, selectedModel);
      setEstimatedCost(reply.estimated_cost.toString());
      if (reply.data) {
        setTableData(reply.data);
      }
      setMessages(prevMessages => [...prevMessages, { type: 'text', content: reply.output, timestamp: new Date(), sender: 'Assistant' }]);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  
  return (
    <div className="App">
      <Header estimatedCost={estimatedCost} selectedModel={selectedModel} onModelChange={handleModelChange} />
      <div style={{ display: 'flex', height: '800px' }}> {/* Flex container */}
        <ResizableBox
          width={width}
          height={300}
          onResize={onResize}
          minConstraints={[100, 300]}
          maxConstraints={[800, 300]}
          handle={<span className="react-resizable-handle react-resizable-handle-e"></span>}
        >
          <AIChatBox messages={messages} handleSendMessage={handleSendMessage} />
        </ResizableBox>
  
        <div style={{ flex: 1, overflow: 'auto', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {tableData && tableData.length > 0 && (
            <div style={{ width: '100%', height:'90%', overflow: 'auto' }}>
              <BasicTable data={tableData} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
  
  
}

export default App;
