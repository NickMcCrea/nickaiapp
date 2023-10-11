import React from 'react';
import { Paper } from '@mui/material'; // Keep Paper for styling
import ChatHistory from './ChatHistory';
import InputWithSendButton from './InputWithSendButton';
import { Message } from './ChatHistory';

type AIChatBoxProps = {
  messages: Message[];
  handleSendMessage: (content: string) => Promise<void>;
};

const AIChatBox: React.FC<AIChatBoxProps> = ({ messages, handleSendMessage }) => {
  return (
    <Paper elevation={1} style={{ padding: '20px', height: '100vh' }}>
    <InputWithSendButton onSubmit={handleSendMessage} />
      <ChatHistory messages={messages} />
    </Paper>
  );
};

export default AIChatBox;
