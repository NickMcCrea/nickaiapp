import { Stack, Typography, Box } from '@mui/material';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import React from 'react';

export interface Message {
  type: 'text' | 'image' | 'other';
  content: string;
  timestamp: Date;
  sender: string;
}

interface ChatHistoryProps {
  messages: Message[];
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages }) => {
  return (
    <Stack spacing={2} sx={{ width: '100%', overflowY: 'auto', padding: '16px' }}>
      {messages.map((message, index) => (
        <Box display="flex" alignItems="flex-start" key={index}>
          {message.type === 'text' && <ChatBubbleOutlineIcon fontSize="small" style={{ marginTop: '6px', marginRight: '8px' }} />}
          <Box>
            <Typography variant="body1">
           
             <strong> {message.sender}:</strong>  {message.content}

            </Typography>
          
          </Box>
        </Box>
      ))}
    </Stack>
  );
};

export default ChatHistory;
