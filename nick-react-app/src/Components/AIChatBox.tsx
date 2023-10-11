import React from 'react';
import { Box, Paper } from '@mui/material'; // Keep Paper for styling

import ChatHistory from './ChatHistory';
import InputWithSendButton from './InputWithSendButton';
import { Message } from './ChatHistory';

type AIChatBoxProps = {
  messages: Message[];
  handleSendMessage: (content: string) => Promise<void>;
};

const AIChatBox: React.FC<AIChatBoxProps> = ({ messages, handleSendMessage }) => {
  return (
    <Box style={{ padding: '20px', height: '80vh' }}>
    <InputWithSendButton onSubmit={handleSendMessage} />
      <ChatHistory messages={messages} />
    </Box>
  );
};

export default AIChatBox;
