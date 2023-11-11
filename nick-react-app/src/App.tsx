import { useState, useEffect, useCallback } from 'react';
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



const dataSets: any[] = [];

function App() {
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
  const [dataSourceNames, setDataSourceNames] = useState<string[]>([]);
  const [catalogueCommentary, setCatalogueCommentary] = useState<string>("");
  const [fadeIn, setFadeIn] = useState(false);
  const [width, setWidth] = useState(600); // Default width for the resizable panel
  const [rightPanelWidth, setRightPanelWidth] = useState(window.innerWidth - width); // Width for the right panel
  const [chatService, setChatService] = useState<ChatService | null>(null);



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





  const renderChart = () => {

    //if current funnction call is bar chart, set to bar.
    //declare chartdata, it can be bar or line or plain data
    let chartData: BarChartData[] | LineChartData[] | PieChartData[] = [];
    if (currentFunctionCall === "fetch_bar_chart_data") 
      chartData = barChartData;
    if (currentFunctionCall === "fetch_line_chart_data") 
      chartData = lineChartData;
    if (currentFunctionCall === "fetch_data")
      chartData = tableData;
    if (currentFunctionCall === "fetch_pie_chart_data")
      chartData = pieChartData;
      
    // Set the chart type based on the current function call
    let chartType: 'bar' | 'line' | 'table' | 'pie' = 'bar';
    if (currentFunctionCall === "fetch_line_chart_data") 
      chartType = 'line';    
    if (currentFunctionCall === "fetch_data") 
      chartType = 'table';
    if (currentFunctionCall === "fetch_pie_chart_data")
      chartType = 'pie';
    

    //set an overflow variable to be off for charts, auto for table
    let overflowValue = "auto";
    if (currentFunctionCall === "fetch_data") 
      overflowValue = "auto";
    else 
      overflowValue = "hidden";  

    if (chartData.length > 0) {
      return (
        <div style={{ width: '80%', height: '80%', overflow: overflowValue } }>
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

  const handleSendMessage = async (content: string) => {


    if (chatService) {
      setMessages([...messages, { type: 'text', content, timestamp: new Date(), sender: 'You' }]);


      try {
        const reply = await chatService.sendMessage(content, selectedModel);
        setEstimatedCost(reply.estimated_cost.toString());


        if(reply.function_call)
          setCurrentFunctionCall(reply.function_call.name);


        if (reply.metaData) {
          dataSets.length = 0; // Clear dataSets
          dataSets.push(reply.metaData); // Add reply.metaData to dataSets

          // Parse the metadata if it's a string, or use it directly if it's already an object
          const metaDataObject = typeof reply.metaData === 'string' ? JSON.parse(reply.metaData) : reply.metaData;
          setMetaData(metaDataObject);

        }
        else {
          console.log("No meta data")
        }

        // If the reply is from a query_meta_data function call
        if (reply.function_call && reply.function_call.name === "query_data_catalogue") {
          // Parse the JSON output
          const outputObject = JSON.parse(reply.output);
          setDataSourceNames(outputObject.data_source_names);
          
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
           
            //if the function call is clear data, clear the data
            if (reply.function_call.name === "clear") {
              setTableData([]);
              setMetaData([]);
              setBarChartData([]);
              setLineChartData([]);
              setMessages([]);
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
      <div style={{ display: 'flex', height: '900px' }}> {/* Flex container */}
        <ResizableBox width={width} height={300} onResize={onResize} minConstraints={[100, 300]} maxConstraints={[800, 300]} handle={<span className="react-resizable-handle react-resizable-handle-e"></span>}>
       {/*    <p>Give me a bar chart of revenues from the financial data set.</p>
          <p>Give me a time series of balances from the trial balance.</p>
          <p>Give me 10 sample rows from the spotify data.</p> 
          <p>Show me the data catalogue</p> 
          <p>Show me the restaurant data structure</p>  */}
          <AIChatBox messages={messages} handleSendMessage={handleSendMessage} />
        </ResizableBox>

        <div style={{ flex: 1, display: 'flex', overflow: 'auto', alignItems: 'center', justifyContent: 'center' }}>      

          {currentFunctionCall === "fetch_meta_data" && dataSets && dataSets.length > 0 && (
            <div style={{ width: '80%', height: '70%' }}>
              <MetaDataCollectionDisplay dataSets={dataSets} />
            </div>
          )}

          {
            ["fetch_bar_chart_data", "fetch_line_chart_data","fetch_pie_chart_data", "fetch_data"].includes(currentFunctionCall) && renderChart()
          }

          {currentFunctionCall === "query_data_catalogue" && dataSourceNames.length > 0 && (
            <div style={{ width: '90%', height: '90%', overflow: 'auto' }}>
              <DataSourceCatalogueDisplay dataSources={dataSourceNames} commentary={catalogueCommentary} />
            </div>
          )}


        </div>
      </div>
    </div>
  );


}

export default App;
