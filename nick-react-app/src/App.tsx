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
import BasicTable from './Components/Charts/BasicTable';
import MetaDataDisplaySimple from './Components/MetaDataDisplay/MetaDataDisplaySimple';
import MetaDataCollectionDisplay from './Components/MetaDataDisplay/MetaDataDisplayCards';
import SimpleBarChart, { BarChartData } from './Components/Charts/SimpleBarChart';
import SimpleLineChart, {LineChartData} from './Components/Charts/SimpleLineChart';
import ProgressData from './Services/ChatService';




const dataSets: any[] = [];

function App() {
  // Add a state to keep track of the current function call
  const [currentFunctionCall, setCurrentFunctionCall] = useState<string>('');

  const [messages, setMessages] = useState<Message[]>([]);
  const [estimatedCost, setEstimatedCost] = useState<string>("");
  const [selectedModel, setSelectedModel] = useState('GPT3.5');
  const [tableData, setTableData] = useState<any[]>([]);
  const [metaData, setMetaData] = useState<any[]>([]);
  const [barChartData, setBarChartData] = useState<BarChartData[]>([]);
  const [lineChartData, setLineChartData] = useState<LineChartData[]>([]);


  const [width, setWidth] = useState(600); // Default width for the resizable panel
  const [rightPanelWidth, setRightPanelWidth] = useState(window.innerWidth - width); // Width for the right panel

  // Instantiate ChatService once for the entire lifecycle of the component
  // Move the instantiation inside useEffect to prevent re-instantiation on every render
  const [chatService, setChatService] = useState<ChatService | null>(null);
  const handleProgress = (progressData: ProgressData) => {
    console.log('Received progress update:', progressData);
    // You can now set this data to state, if needed, or perform other actions
  };
  useEffect(() => {
    // Instantiate ChatService and store it in the state
    const service = new ChatService("http://localhost:5001");
    setChatService(service);

    service.on('progress', (progressData: any) => 
    {
      //set a message using the progressData.status
      setMessages(prevMessages => [...prevMessages, { type: 'text', content: progressData.status, timestamp: new Date(), sender: 'Working' }]);
    });

    // Cleanup function to be called on component unmount
    return () => {
      service.cleanup(); // Cleanup the chat service when the component unmounts
    };
  }, []); // Empty dependency array to ensure this effect runs once on mount and once on unmount


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
    

    if (chatService) {
      setMessages([...messages, { type: 'text', content, timestamp: new Date(), sender: 'You' }]);


    try {
      const reply = await chatService.sendMessage(content, selectedModel);
      setEstimatedCost(reply.estimated_cost.toString());
      // If the reply is from a query_meta_data function call
      if (reply.function_call && reply.function_call.name === "query_meta_data") {
        // Parse the JSON output
        const outputObject = JSON.parse(reply.output);

        // Extract data source names and commentary
        const { data_source_names, commentary } = outputObject;

        // Construct a formatted JSX message
        const metaDataMessage = (
          <span>
            Data Source(s): <strong>{data_source_names.join(', ')}</strong>. {commentary}
          </span>
        );




        // Add the JSX formatted message to the chat history
        setMessages(prevMessages => [...prevMessages, { type: 'jsx', content: metaDataMessage, timestamp: new Date(), sender: 'Assistant' }]);
      } else {
        // Handle other messages as before
        if (reply.data) {
          setTableData(reply.data);
        }

        //check function call name and set current function call
        if (reply.function_call) {
          if (reply.function_call.name === "fetch_meta_data") {
            setCurrentFunctionCall("fetch_meta_data");
          }
          if (reply.function_call.name === "fetch_data") {
            setCurrentFunctionCall("fetch_data");

          }
          if (reply.function_call && reply.function_call.name === "fetch_bar_chart_data") {
            // Assuming the data is in the format required by the chart
            if (Array.isArray(reply.data)) {
              const formattedData = reply.data.map(item => ({
                ...item,
                Total: parseFloat(item.Total)
              }));
              setBarChartData(formattedData as BarChartData[]);
              setCurrentFunctionCall("fetch_bar_chart_data");
            } else {
              // Handle the case where reply.data is undefined or not an array
              console.error('Received data is not an array', reply.data);
            }
          }
          if(reply.function_call && reply.function_call.name === "fetch_line_chart_data"){
            if (Array.isArray(reply.data)) {

              setLineChartData(reply.data as LineChartData[]);
              setCurrentFunctionCall("fetch_line_chart_data");
            }

          }
        }

        if (reply.metaData) {
          dataSets.length = 0; // Clear dataSets
          dataSets.push(reply.metaData); // Add reply.metaData to dataSets
          setMetaData(dataSets);
          console.log("dataSets: " + reply.metaData); // Log the data
        }

        // Add the assistant's reply to the chat history
        setMessages(prevMessages => [...prevMessages, { type: 'text', content: reply.output, timestamp: new Date(), sender: 'Assistant' }]);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    }
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

        <div style={{ flex: 1, display: 'flex', overflow: 'auto', alignItems: 'center', justifyContent: 'center' }}>
          {currentFunctionCall === "fetch_data" && tableData && tableData.length > 0 && (
            <div style={{ width: '90%', height: '80%', overflow: 'auto' }}>
              <BasicTable data={tableData} />
            </div>
          )}

          {currentFunctionCall === "fetch_meta_data" && dataSets && dataSets.length > 0 && (
            <MetaDataCollectionDisplay dataSets={dataSets} />
          )}

          {currentFunctionCall === "fetch_bar_chart_data" && barChartData.length > 0 && (
          <div style={{ width: '80%', height: '70%'}}>
              <SimpleBarChart data={barChartData} />
              </div>
       
          )}

          {currentFunctionCall === "fetch_line_chart_data" && lineChartData.length > 0 && (
           <div style={{ width: '80%', height: '70%'}}>
              <SimpleLineChart data={lineChartData} />
              </div>
          )}


        </div>
      </div>
    </div>
  );


}

export default App;
