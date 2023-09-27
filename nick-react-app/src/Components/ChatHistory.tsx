import { Stack, Typography } from '@mui/material';
import React from 'react';

export interface Message {
  type: 'text' | 'image' | 'other'; // extended to handle image type
  content: string;
  timestamp: Date;
}

interface ChatHistoryProps {
  messages: Message[];
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages }) => {
  return (
    <Stack spacing={2} sx={{ width: '100%', overflowY: 'auto', padding: '16px' }}>
      {messages.map((message, index) => (
        <Stack direction="column" key={index} spacing={1}>
          {message.type === 'text' && <Typography>{message.content}</Typography>}
          {message.type === 'image' && <img src={message.content} alt="message content" style={{ maxWidth: '100%' }} />}
          {message.type === 'other' && <Typography fontStyle="italic">{message.content}</Typography>}
        </Stack>
      ))}
    </Stack>
  );
};

export default ChatHistory;
