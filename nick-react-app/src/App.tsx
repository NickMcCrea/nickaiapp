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
import FieldCard from './Components/FieldCard';
import DataSet from './Components/DataSet';
import DataSetCollection from './Components/DataSetCollection';

const jsonString2 = `{
  "name": "spotify_track_data",
  "description": "Data of music tracks from Spotify with ranking and audio features",
  "fields": [
      {
          "fieldName": "spotify_id",
          "fieldDescription": "Unique identifier for the Spotify track",
          "fieldType": "STRING"
      },
      {
          "fieldName": "name",
          "fieldDescription": "Name of the track",
          "fieldType": "STRING"
      },
      {
          "fieldName": "artists",
          "fieldDescription": "Artists performing the track",
          "fieldType": "STRING"
      },
      {
          "fieldName": "daily_rank",
          "fieldDescription": "Daily rank of the track",
          "fieldType": "INTEGER"
      },
      {
          "fieldName": "daily_movement",
          "fieldDescription": "Daily movement in the track's rank",
          "fieldType": "INTEGER"
      },
      {
          "fieldName": "weekly_movement",
          "fieldDescription": "Weekly movement in the track's rank",
          "fieldType": "INTEGER"
      },
      {
          "fieldName": "country",
          "fieldDescription": "Country in which the track is ranked",
          "fieldType": "STRING"
      },
      {
          "fieldName": "snapshot_date",
          "fieldDescription": "Date of the data snapshot",
          "fieldType": "DATE"
      },
      {
          "fieldName": "popularity",
          "fieldDescription": "Popularity score of the track",
          "fieldType": "INTEGER"
      },
      {
          "fieldName": "is_explicit",
          "fieldDescription": "Flag indicating if the track has explicit content",
          "fieldType": "BOOLEAN"
      },
      {
          "fieldName": "duration_ms",
          "fieldDescription": "Duration of the track in milliseconds",
          "fieldType": "INTEGER"
      },
      {
          "fieldName": "album_name",
          "fieldDescription": "Name of the album the track is from",
          "fieldType": "STRING"
      },
      {
          "fieldName": "album_release_date",
          "fieldDescription": "Release date of the album",
          "fieldType": "DATE"
      },
      {
          "fieldName": "danceability",
          "fieldDescription": "Danceability score of the track",
          "fieldType": "FLOAT"
      },
      {
          "fieldName": "energy",
          "fieldDescription": "Energy score of the track",
          "fieldType": "FLOAT"
      },
      {
          "fieldName": "key",
          "fieldDescription": "Key the track is in",
          "fieldType": "INTEGER"
      },
      {
          "fieldName": "loudness",
          "fieldDescription": "Loudness of the track in decibels",
          "fieldType": "FLOAT"
      },
      {
          "fieldName": "mode",
          "fieldDescription": "Mode of the track (major or minor)",
          "fieldType": "INTEGER"
      },
      {
          "fieldName": "speechiness",
          "fieldDescription": "Speechiness score of the track",
          "fieldType": "FLOAT"
      },
      {
          "fieldName": "acousticness",
          "fieldDescription": "Acousticness score of the track",
          "fieldType": "FLOAT"
      },
      {
          "fieldName": "instrumentalness",
          "fieldDescription": "Instrumentalness score of the track",
          "fieldType": "FLOAT"
      },
      {
          "fieldName": "liveness",
          "fieldDescription": "Liveness score of the track",
          "fieldType": "FLOAT"
      },
      {
          "fieldName": "valence",
          "fieldDescription": "Valence score of the track",
          "fieldType": "FLOAT"
      },
      {
          "fieldName": "tempo",
          "fieldDescription": "Tempo of the track in beats per minute",
          "fieldType": "FLOAT"
      },
      {
          "fieldName": "time_signature",
          "fieldDescription": "Time signature of the track",
          "fieldType": "INTEGER"
      }
  ]
}
`

const jsonString = `{
  "name": "restaurant_info",
  "description": "Information about various restaurants including ratings, cuisine, pricing, and safety measures",
  "fields": [
      {
          "fieldName": "restaurant_name",
          "fieldDescription": "Name of the restaurant",
          "fieldType": "STRING"
      },
      {
          "fieldName": "rating",
          "fieldDescription": "Average rating of the restaurant",
          "fieldType": "FLOAT"
      },
      {
          "fieldName": "cuisine",
          "fieldDescription": "Types of cuisines offered by the restaurant",
          "fieldType": "STRING"
      },
      {
          "fieldName": "average_price",
          "fieldDescription": "Average price for one person",
          "fieldType": "STRING"
      },
      {
          "fieldName": "average_delivery_time",
          "fieldDescription": "Average time taken for delivery",
          "fieldType": "STRING"
      },
      {
          "fieldName": "safety_measure",
          "fieldDescription": "Safety measures followed by the restaurant",
          "fieldType": "STRING"
      },
      {
          "fieldName": "location",
          "fieldDescription": "Geographical location of the restaurant",
          "fieldType": "STRING"
      }
  ]
}`;

const dataSets = [
  JSON.parse(jsonString),
  JSON.parse(jsonString2),
  // ... more parsed JSON objects ...
];

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
      <div style={{ display: 'flex' , height: '800px'}}> {/* Flex container */}
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
          {tableData && tableData.length > 0 && (
            <div style={{ width: '100%', height:'90%', overflow: 'auto' }}>
              <BasicTable data={tableData} />
            </div>
          )}
          
        <DataSetCollection dataSets={dataSets} />
          
      

        </div>
      </div>
    </div>
  );
  
  
}

export default App;
