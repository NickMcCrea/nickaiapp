// MiniAskAI.tsx
import React, { useState } from 'react';
import InputWithSendButton from './InputWithSendButton'; // assuming this is in the same directory
import BasicTable from './Charts/BasicTable';
import LinearProgress from '@mui/material/LinearProgress'; // Import a progress indicator component


interface MiniAskAIProps {
    dataSourceName: string;
}

const MiniAskAI: React.FC<MiniAskAIProps> = ({ dataSourceName }) => {


    //store meta data we get back from the api
    const [tableData, setTableData] = useState<any>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false); // New state for loading indicator



    const handleAskSubmit = async (input: string) => {
        const url = 'http://127.0.0.1:5001/ask_specific';
        const requestBody = {
            input: input,
            data_source_name: dataSourceName
        };

        setIsLoading(true); 

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });

            const data = await response.json();

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
