// MiniAskAI.tsx
import React, { useState } from 'react';
import InputWithSendButton from './InputWithSendButton'; // assuming this is in the same directory
import BasicTable from './Charts/BasicTable';
import LinearProgress from '@mui/material/LinearProgress'; // Import a progress indicator component
import ChatService from '../Services/ChatService'; // Import the ChatService


interface MiniAskAIProps {
    dataSourceName: string;
    chatService: ChatService;
}

interface MiniAskAIResponse {
    data: any;
}

const MiniAskAI: React.FC<MiniAskAIProps> = ({ dataSourceName, chatService: ChatService }) => {


    //store meta data we get back from the api
    const [tableData, setTableData] = useState<any>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false); // New state for loading indicator

    //set the chat service
    const chatService = ChatService;




    const handleAskSubmit = async (input: string) => {
      
        const requestBody = {
            input: input,
            data_source_name: dataSourceName
        };

        setIsLoading(true);

        try {
            const data = await chatService.restService.makeRequest<MiniAskAIResponse>('ask_specific', requestBody);
            //set the table data
            setTableData(data.data);
            console.log('Response from MiniAskAI:', data);

        } catch (error) {
            console.error('Error in MiniAskAI:', error);
        }
        finally {
            setIsLoading(false); // Set loading to false when request completes
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{ marginTop: '20px' }}>
                <InputWithSendButton onSubmit={handleAskSubmit} />
            </div>


            <div>
                {isLoading ? (
                    <LinearProgress /> // Show progress indicator when loading
                ) : (
                    tableData && <BasicTable data={tableData} />
                )}
            </div>


        </div>
    );
};

export default MiniAskAI;
