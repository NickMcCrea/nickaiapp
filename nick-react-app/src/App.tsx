import { CSSProperties, useState, useEffect, useCallback } from 'react';
import ChatService, { ProgressData } from './Services/ChatService';
import { Message } from './Components/ChatHistory';
import Header from './Components/Header';
import AIChatBox from './Components/AIChatBox';
import "react-resizable/css/styles.css";
import './App.css';
import MetaDataCollectionDisplay from './Components/MetaDataDisplay/MetaDataDisplayCards';
import { BarChartData } from './Components/Charts/SimpleBarChart';
import { LineChartData } from './Components/Charts/SimpleLineChart';
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

  const fetchCatalogue = async () => {
    try {
      // Make a GET request to the specified URL
      const response = await fetch('http://localhost:5001/get_catalogue');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // Parse the response JSON
      const data = await response.json();
  
      // Update the state with the fetched data
      setDataCatalogueMeta(data);
      setActiveContent("catalogue");
      toggleChatBoxVisibility();
    } catch (error) {
      console.error("Failed to fetch catalogue:", error);
      // You may want to handle errors more gracefully in a real app
    }
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
  const [fadeIn, setFadeIn] = useState(false);

  const [chatService, setChatService] = useState<ChatService | null>(null);
  const [dataCatalogueMeta, setDataCatalogueMeta] = useState<DataSourceMetaDeta[]>([]);

  const [activeContent, setActiveContent] = useState<string | null>(null); // New state for active content

  const [pipelineData, setPipelineData] = useState<PipelineStep[]>([]);


  const onPowerBiClick = (powerBiValue: string) => {
    console.log('Power BI Clicked with value:', powerBiValue);
    setActiveContent("powerbi");
    // Add any additional logic you need here
  };
  


  useEffect(() => {
    // Instantiate ChatService and store it in the state
    const service = new ChatService("http://localhost:5001");
    setChatService(service);

    // Subscribe to the 'progress' event
    service.socketClient.subscribe('progress', (progressData: ProgressData ) => {
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
            <DataZoneDisplay dataSources={dataCatalogueMeta} onPowerBiClick={onPowerBiClick} commentary='' />
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

      case "powerbi":
        return (
          <div style={{ width: '90%', height: '90%' }}> {/* Ensure this container has width and height */}
            <PowerBIReport embedUrl='https://app.powerbi.com/reportEmbed?reportId=f6bfd646-b718-44dc-a378-b73e6b528204\u0026groupId=be8908da-da25-452e-b220-163f52476cdd\u0026w=2\u0026config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVVTLU5PUlRILUNFTlRSQUwtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQiLCJlbWJlZEZlYXR1cmVzIjp7InVzYWdlTWV0cmljc1ZOZXh0Ijp0cnVlfX0%3d' 
            reportId='f6bfd646-b718-44dc-a378-b73e6b528204' accessToken='H4sIAAAAAAAEACWWxQ70CA6E3-W_ZqQwjTSHMDPnFuhQhzlZ7btvr-ZuWfJX5bL_88fOnn7Kyj9__5kzd3Bl06dsX19eytzFrhR6e9Q49mZvZlhynaOUspPKN1OuLedMNoe7GRJmzOBn0ZcEW_2yoBsFoo1Y9m62nFtIxbZYITdXz8NsXnFQwxvHbK-XGq3yrBp8wWj_nlJzTqH9RuymdVxK1S8gSIsZKlF0noQqeESVrtbMwQumwyMMFgqJdGEx3gINiBA_g0WY3wZi5hP1zh_bTWKaUfjGmdd67rhPsKST5PV2W3NDMVsD7jyV36YnLE3Z1rmMRi4DyGa_MrNYRpoAYf-utGBIRkaiCdquvUh0704pYptl0XeUMNeEwIlA2_gsZ2qby5G7V1ViIiYkyqZTL7YR8XwIBpIWEL6Z3jsdkbJAZBGou6pS9_nGLtkQuzuXT49gfa0PHHfAyBeSyB6BmxXFp-XQHsFVYVvSwoRgUn_67pfCY6G61OjN0QWi2HQElKKrbXypN9Wdd7pEMGM_ZO1dukK1NRGO0i1Q3-wC8CF2EuF3ackYgrFwnTHUxlltJwCjPu7pcOyo-mZtizzDLuh12Isnpdl63qX-05WOVN0XNYM0CSENG0UQC5WZAFntXWChf98v5N7Psn32AkndB396LNsDsMyFVJRdd0CXAikxiOwOf68bp4932xuuPGHe136oVUSRu7ZbmnDaz3WfnSskVm6p-KARKqdmCSnHUETneCB0oRTz5zfmypkWmnUHpj6yDUBBqlGcm1hdLROe43atnHt00vakTWSKX9tO1J_-dmc0bFgqxCeRZ4fJ9UAU6v3uehqXdV-OBL3wUcrodHUslmcP7LSu2osndsyCYtFFz4ODyemhDFZVTd3puRuikTAzHK52jbn-OMRITGHZMfhDXEt06ag8KTq6tAhu3h2Ykox9oSp0xN5gGJPM2_7hrHPzvVJeK4UuIbPmM4AlFSMFIB61SduJR5YLWtYyJ1TJlUreyclqgi2bazrlbCPMFuGdYoUrWBeUoLVBwgUQCehS-ogYZnT94h0tOGdQPqHLz0AvA9VMuEP7YZJnb1kcOiS_XS_yh5nxgr3uRU74OoWpMEiWleMwln8fWOXdVHQX2LSN927FBOZy5oIcI6dwUxHSemynjIxAncUUadvtkYJAKTgxd_JRwy_MisbYbqCvEdAEWLYoaF3ClsTzFuK8dPy0EiJZH-mO-IByFo0X91jU3a9TBaeIzxe0DawU2gNq4pQILhbGqFAzNh5_aLvrgph0GDNHBTprt8t2g0lGaN8cATaCmTmDLhGwkZpeMVxIWmCpNM_VVncm76Q1oClmIGjwKLibLwXOkboueA_waSsSt8cV9Zqa9FVXSDFOkapuXteRR5nfWGxdssfiSl-t2gg7wNIqZPISYhA0DmkDazY8mSP9M5Xr2ITIt0KcUVkG2GIERFZVd5EfWYa9p64hWzwLJ_AjQPVqgCQfDZFtvmdfEKqPOUXaefmqVCqJsknR--jHWSlyUIDoPq-9_q-f79K9epy42B5fZ_3u5B7Ez54-6FupGyOH6yHcTqgj355Aaaq7q-66R-6hMJGBIWkqZiHYj4j8kn3LFjM6o6voDl9Ido7ZaXMNxpKDS3QbN4RLzgyMWeUESXw0tx7kfntcNPRRxRE33MvM0bOjpvaWhtuwnWBAHpZdADO4vSYIdnBnPvtReeTrIiqd_rZk5IVKlw1pY2o1yXBH3R56LDcOmCRoa8eyontvusMHR2fBNObNZV3Ae592KD5yso_AbuBkVHRUztfK4UGDws4sRhQuMJD3EhL3TLvVXgAsM3TfYYLalplOdEFXj0jeryjsTBsj0JSd1p29PapIVif0vGwo_OlIFCpUFUQMZ7vnMV83DycxCYChzUnwuYJlAHY4EdR6xlJh-b2m4Oteas0iEWk3t8nRBjSiaacqkB-xTSVtzb2lP39ZVqDbD9va0qG7paIPr9IlFV2u0vQmr6RRLTo8rA1-5V2kadbjSPyM4YDkmfDKHJ4y5UY1MNSziUkNX2GQ2tio0Hc_SlbEPDJTnUUeOC_x9a26DSgGdp-wL7OiUBxqWOU7x3TOJoQP9sQK9pMCzD-WbOsYN6Lum_6KvmXcuFV9hjExb62h0zocKHtAXEePeCsPZU0HW0wEBk2pKo6di3EPMyFa02AlHZabimLNGq5Om3IsWIbvVdYPmUSoSJWZihHFPUfwKMSrGiIbYRqnd6UbxlYriWcw6JM6aGkCs3JExOxTu5PJz-z_VcU3oNiRjwu9MuVmYZa2sGSL4desp3Cmm3XsKuwoT8jadFrc-kyzLqIDWskpnowdp-4NTvioO8D7krYRjCNt2URdbAnif7nbi3lDIDy9DEaIdxLMnfflw7rTRTPgAcFmytfzVEL0TqHvUHxmApqvG1N-J1oq4_CFCMTRKpdwdKqMUtbzd_RJqWY9eTQX_fYoVrOE8gbPqLyR8266cKy4lc8cRiboCG2ocN6GiMN76Pg7_1AGiKmWiox9P7_cc0Zruv75589ff7j1mfdJ-zy_N62KJdfuvCQJyRkZPNU_nuwGgKx-qA4tLv7h4DvXLQ80shj0VQVIP0l08m9GIa7fY8CCeB_G7UYTZjN-jFlwl5GwHikfOMsRMmzenmyvM-N0tGYaZuYQKAejHcqtnfbz_oKbhcBJfSkuuLQ1qmDobTzai2mL17eTpOW0S3BVwojdMNlkz9N4s9vsKcBvLKOmiCROXpwcbXczzWldNmbgK3nNDoYapeB8l91fYfoEQWS0mLl6FLxWcoT7MjjQcdXXgDa8EuMU-45f-I2JMtTGT16ZgOcY9QfPNDRi2w7HyhUOr_aQcQGqHb_gsY_B-oof2GEM2YJ41RHvdlyj0LrkxhsJ1_9ifubmsyrhjzItBHrM-_rRSd_tcfEQXEnvXzG8th6z_Vg_vzJNsT7RcaZAeWDpKLQfZPM3Pedzcuh2H90YfuqeswbMCUM_v1hUJ2_sW7XUeZyaBGnQraPCMjwNZd7JadKqxdmz1PLRCC3QYfLBNbiz2HCpG3wO-n0gtS9iwAm16U1MrQ0Ff1nVnY0duMiCtCxsv_ckWJhOFOnzAnhL2ebHCj-hEzIjZOOCrWBduhBmsoKw8mMxXb8zjjlVb5Cefqhk2cMydHH4h-G186itvoB0jmV0OVXfxCTFSNp5EEBAHk7gkCM6omdVCc7I0b6dQY0tqSgi4FFnOtL2WiT83_fCSrdwCSppnyiGMLyl1URnPkFGArCTFmpkvSEDk5-gwZTi8pShFpkf5v_-D9kgNX-aDAAA.eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVVTLU5PUlRILUNFTlRSQUwtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQiLCJleHAiOjE3MDE2MzI5NDUsImFsbG93QWNjZXNzT3ZlclB1YmxpY0ludGVybmV0Ijp0cnVlfQ==' />
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


        if (reply.metadata) {
          dataSets.length = 0; // Clear dataSets
          dataSets.push(reply.metadata); // Add reply.metaData to dataSets
          setMetaData(reply.metadata);
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


          if (reply.metadata) {

            if (Array.isArray(reply.metadata)) {
              setDataCatalogueMeta(reply.metadata as DataSourceMetaDeta[]);
            }


            const newDataSourceNames = [];
            const newDataSetDescriptions = [];
            for (const item of reply.metadata) {
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
              console.log('reply.metaData', reply.metadata);
              var pipelineDataTest = reply.metadata as PipelineStep[];
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
      <IconButton onClick={fetchCatalogue} style={catalogueButtonStyle}>
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
