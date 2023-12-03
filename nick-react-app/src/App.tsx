import { CSSProperties, useState, useEffect, useCallback } from 'react';
import { ResizableBox } from 'react-resizable';
import ChatService from './Services/ChatService';
import { Message } from './Components/ChatHistory';
import Header from './Components/Header';
import AIChatBox from './Components/AIChatBox';
import "react-resizable/css/styles.css";
import './App.css';
import MetaDataCollectionDisplay from './Components/MetaDataDisplay/MetaDataDisplayCards';
import { BarChartData } from './Components/Charts/SimpleBarChart';
import { LineChartData } from './Components/Charts/SimpleLineChart';
import DataSourceCatalogueDisplay from './Components/DataCatalogueDisplay';
import GenericChart from './Components/Charts/GenericChart';
import { PieChartData } from './Components/Charts/SimplePieChart';
import { ScatterChartData } from './Components/Charts/SimpleScatterChart';
import { DataSourceMetaDeta } from './Components/DataSourceMetaDeta';
import PipelineVisualiser, { PipelineStep } from './Components/Charts/PipelineVisualiser';
import PowerBIReport from './Components/PowerBIComponent';
import DataZoneDisplay from './Components/DataZoneDisplay';
import IconButton from '@mui/material/IconButton';
import ChatIcon from '@mui/icons-material/Chat';
import FolderCopyIcon from '@mui/icons-material/FolderCopy';



const dataSets: any[] = [];

function App() {

   // State to control the visibility of AIChatBox
   const [isChatBoxVisible, setIsChatBoxVisible] = useState(true);


   // Toggle function for AIChatBox visibility
   const toggleChatBoxVisibility = () => {
     setIsChatBoxVisible(!isChatBoxVisible);
   };

   const addCatalogueMessage = () => {
    const newMessage = { 
      type: 'text', 
      content: 'Show me the catalogue please', 
      timestamp: new Date(), 
      sender: 'You' 
    };

    setMessages([...messages, { type: 'text', content: newMessage.content, timestamp: newMessage.timestamp, sender: newMessage.sender}]);

    // If you also want to simulate sending this message (like a user would do)
    handleSendMessage('Show me the catalogue please');
  };


   // Dynamic styles for panels based on AIChatBox visibility
  const leftPanelStyle = {
    width: isChatBoxVisible ? '25%' : '0%',
    transition: 'width 0.3s ease-in-out',
    overflow: 'hidden',
  };

  const rightPanelStyle = {
    width: isChatBoxVisible ? '75%' : '100%',
    transition: 'width 0.3s ease-in-out',
    display: 'flex',
    overflow: 'auto',
    alignItems: 'center',
    justifyContent: 'center',
  };

  const chatVisibleStyle: CSSProperties  = {
    position: 'absolute', // Position it over the other components
    bottom: 0,
    left: 0,
    zIndex: 1000, // Ensure it's above other elements
  };

  const catalogueButtonStyle: CSSProperties  = {
    position: 'absolute', // Position it over the other components
    bottom: 0,
    left: 40,
    zIndex: 1000, // Ensure it's above other elements
  };

  // Add a state to keep track of the current function call
  const [currentFunctionCall, setCurrentFunctionCall] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [estimatedCost, setEstimatedCost] = useState<string>("");
  const [selectedModel, setSelectedModel] = useState('GPT4');
  const [tableData, setTableData] = useState<any[]>([]);
  const [metaData, setMetaData] = useState<{ [key: string]: any }>({});
  const [barChartData, setBarChartData] = useState<BarChartData[]>([]);
  const [lineChartData, setLineChartData] = useState<LineChartData[]>([]);
  const [pieChartData, setPieChartData] = useState<PieChartData[]>([]);
  const [scatterChartData, setScatterChartData] = useState<ScatterChartData[]>([]);
  const [dataSourceNames, setDataSourceNames] = useState<string[]>([]);
  const [catalogueCommentary, setCatalogueCommentary] = useState<string>("");
  const [fadeIn, setFadeIn] = useState(false);

  const [chatService, setChatService] = useState<ChatService | null>(null);
  const [dataCatalogueMeta, setDataCatalogueMeta] = useState<DataSourceMetaDeta[]>([]);

  const [activeContent, setActiveContent] = useState<string | null>(null); // New state for active content

  const [pipelineData, setPipelineData] = useState<PipelineStep[]>([]);


  useEffect(() => {
    // Instantiate ChatService and store it in the state
    const service = new ChatService("http://localhost:5001");
    setChatService(service);

    service.on('progress', (progressData: any) => {
      //set a message using the progressData.status
      setMessages(prevMessages => [...prevMessages, { type: 'text', content: progressData.status, timestamp: new Date(), sender: 'Working' }]);
    });

    // Cleanup function to be called on component unmount
    return () => {
      service.cleanup(); // Cleanup the chat service when the component unmounts
    };
  }, []); // Empty dependency array to ensure this effect runs once on mount and once on unmount

  // Use a callback to add the fade-in class when the component mounts
  const toggleFadeIn = useCallback(() => {
    setFadeIn(true);
  }, []);

  useEffect(() => {
    // Whenever the component mounts, we start the fade-in animation
    toggleFadeIn();
  }, [toggleFadeIn]);





  const handleModelChange = (model: string) => {
    setSelectedModel(model);
    console.log(model);
  };


  const renderChart = () => {

    console.log("renderChart: calling renderChart");
    //if current funnction call is bar chart, set to bar.
    //declare chartdata, it can be bar or line or plain data
    let chartData: BarChartData[] | LineChartData[] | PieChartData[] | ScatterChartData[] = [];
    if (activeContent === "bar_chart")
      chartData = barChartData;
    if (activeContent === "line_chart")
      chartData = lineChartData;
    if (activeContent === "table")
      chartData = tableData;
    if (activeContent === "pie_chart")
      chartData = pieChartData;
    if (activeContent === "scatter_chart")
      chartData = scatterChartData;


    // Set the chart type based on the current function call
    let chartType: 'bar' | 'line' | 'table' | 'pie' | 'scatter' = 'bar';
    if (activeContent === "line_chart")
      chartType = 'line';
    if (activeContent === "table")
      chartType = 'table';
    if (activeContent === "pie_chart")
      chartType = 'pie';
    if (activeContent === "scatter_chart")
      chartType = 'scatter';
    if (activeContent === "bar_chart")
      chartType = 'bar';

    console.log("renderChart: Active content is: " + activeContent);


    //set an overflow variable to be off for charts, auto for table
    let overflowValue = "auto";
    if (activeContent === "table")
      overflowValue = "auto";
    else
      overflowValue = "hidden";

    if (chartData.length > 0) {
      return (
        <div style={{ width: '80%', height: '80%', overflow: overflowValue }}>
          <GenericChart
            type={chartType}
            data={chartData}
            metaData={{
              XAxisTitle: metaData["x_axis_title"] || "Default Title",
              YAxisTitle: metaData["y_axis_title"] || "Default Title",
              ChartTitle: metaData["chart_title"] || "Default Title"
            }}
          />
        </div>
      );
    }
    return null;
  };

  // Function to render the active content
  const renderActiveContent = () => {

    console.log("renderActiveContent: Active content is: " + activeContent);
    switch (activeContent) {

      case "bar_chart":
        return renderChart();
      case "line_chart":
        return renderChart();
      case "pie_chart":
        return renderChart();
      case "scatter_chart":
        return renderChart();
      case "table":
        return renderChart();
      case "catalogue":
        return (
          <div style={{ width: '90%', height: '90%', overflow: 'auto' }}>
            <DataZoneDisplay dataSources={dataCatalogueMeta} commentary={catalogueCommentary} />
          </div>
        );
      case "metaData":
        return (
          <div style={{ width: '80%', height: '90%' }}>
            <MetaDataCollectionDisplay dataSets={dataSets} />
          </div>
        );
      case "pipeline":
        return (
          <div style={{ width: '100%', height: '90%' }}> {/* Ensure this container has width and height */}
            <PipelineVisualiser pipelineDefinition={pipelineData} />
          </div>
        );
      default:
        return null;
    }
  };

  const handleSendMessage = async (content: string) => {


    if (chatService) {
      setMessages([...messages, { type: 'text', content, timestamp: new Date(), sender: 'You' }]);


      try {
        const reply = await chatService.sendMessage(content, selectedModel);


        if (reply.function_call)
          setCurrentFunctionCall(reply.function_call.name);


        if (reply.metaData) {
          dataSets.length = 0; // Clear dataSets
          dataSets.push(reply.metaData); // Add reply.metaData to dataSets
          setMetaData(reply.metaData);
        }

        if (reply.function_call) {
          switch (reply.function_call.name) {
            case "fetch_bar_chart_data":
              setActiveContent("bar_chart");
              break;
            case "fetch_line_chart_data":
              setActiveContent("line_chart");
              break;
            case "fetch_pie_chart_data":
              setActiveContent("pie_chart");
              break;
            case "fetch_scatter_chart_data":
              setActiveContent("scatter_chart");
              break;
            case "fetch_data":
              setActiveContent("table");
              break;
            case "query_data_catalogue":
              setActiveContent("catalogue");
              break;
            case "fetch_meta_data":
              setActiveContent("metaData");
              break;
            case "define_new_data_set":
              setActiveContent("pipeline");
              break;

            default:
              console.log("Default active content is: " + activeContent);
              //set active content to whatever it was last time
              setActiveContent(activeContent);

              break;
          }
        }
        else
          setActiveContent(activeContent);

        // If the reply is from a query_meta_data function call
        if (reply.function_call && reply.function_call.name === "query_data_catalogue") {


          if (reply.metaData) {

            if (Array.isArray(reply.metaData)) {
              setDataCatalogueMeta(reply.metaData as DataSourceMetaDeta[]);
            }


            const newDataSourceNames = [];
            const newDataSetDescriptions = [];
            for (const item of reply.metaData) {
              if ('name' in item && 'description' in item) {
                newDataSourceNames.push(item.name);
                console.log(item.name);
                newDataSetDescriptions.push(item.description);
              }
            }

            // Parse the JSON output
            const outputObject = JSON.parse(reply.output);

            setDataSourceNames(outputObject.data_source_names);

            const { data_source_names, commentary } = outputObject;

            // Construct a formatted JSX message
            const metaDataMessage = (
              <span>
                Data Source(s): <strong>{newDataSourceNames.join(', ')}</strong>. {commentary}
              </span>
            );

            // Add the JSX formatted message to the chat history
            setMessages(prevMessages => [...prevMessages, { type: 'jsx', content: metaDataMessage, timestamp: new Date(), sender: 'Assistant' }]);
          }
        } else {
          // Handle other messages as before
          if (reply.data) {
            setTableData(reply.data);
          }

          //check function call name and set current function call
          if (reply.function_call) {

            //if the function call is clear data, clear the data
            if (reply.function_call.name === "clear") {
              setTableData([]);
              setMetaData([]);
              setBarChartData([]);
              setLineChartData([]);
              setMessages([]);
              setActiveContent(null)
              setPipelineData([]);
            }

            if (reply.function_call && reply.function_call.name === "fetch_bar_chart_data") {
              // Assuming the data is in the format required by the chart
              if (Array.isArray(reply.data)) {
                const formattedData = reply.data.map(item => ({
                  ...item,
                  Total: parseFloat(item.Total)
                }));

                //set  bar chart data
                setBarChartData(formattedData)


              } else {
                // Handle the case where reply.data is undefined or not an array
                console.error('Received data is not an array', reply.data);
              }
            }
            if (reply.function_call && reply.function_call.name === "fetch_line_chart_data") {
              if (Array.isArray(reply.data)) {

                setLineChartData(reply.data as LineChartData[]);
              }
            }

            if (reply.function_call && reply.function_call.name === "fetch_pie_chart_data") {
              if (Array.isArray(reply.data)) {

                setPieChartData(reply.data as PieChartData[]);
              }
            }

            if (reply.function_call && reply.function_call.name === "fetch_scatter_chart_data") {
              if (Array.isArray(reply.data)) {

                setScatterChartData(reply.data as ScatterChartData[]);
              }
            }

            if (reply.function_call && reply.function_call.name === "define_new_data_set") {


              //transform metaData to pipeline data
              console.log('reply.metaData', reply.metaData);
              var pipelineDataTest = reply.metaData as PipelineStep[];
              console.log('pipelineDataTest', pipelineDataTest);
              setPipelineData(pipelineDataTest);

            }



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
      <IconButton onClick={toggleChatBoxVisibility} style={chatVisibleStyle}>
        <ChatIcon />
      </IconButton>
      <IconButton onClick={addCatalogueMessage} style={catalogueButtonStyle}>
        <FolderCopyIcon />
      </IconButton>
      <div style={{ display: 'flex', height: 1200 }}> {/* Flex container */}
      < div style={leftPanelStyle}>
          <AIChatBox messages={messages} handleSendMessage={handleSendMessage} />
        </div>
        <div style={rightPanelStyle}>
          {renderActiveContent()}
        </div>
      </div>
    </div>
  );
}




export default App;
