import { Stack, Typography, Box } from '@mui/material';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import React from 'react';
import { styled } from '@mui/system';

const FadeInBox = styled(Box)<{ index?: number }>(({ index = 0 }) => ({
  opacity: 0,
  transform: 'translateY(10px)',
  animation: 'fadein 0.2s forwards',
  animationDelay: `${0.2 * (index)}s`,
  '@keyframes fadein': {
    '0%': {
      opacity: 0,
      transform: 'translateY(10px)',
    },
    '100%': {
      opacity: 1,
      transform: 'translateY(0)',
    },
  },
}));

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
    <Stack 
      spacing={2} 
      sx={{ 
        width: '100%', 
        maxHeight: '100%',  // Set a maximum height
        overflowY: 'auto',  // Enable vertical scrolling
        padding: '0px',
        marginTop: '10px',
        '&::-webkit-scrollbar': {  // Hide scrollbar for Chrome, Safari and Opera
          display: 'none',
        },
        '-ms-overflow-style': 'none',  // Hide scrollbar for IE and Edge
        scrollbarWidth: 'none',  // Hide scrollbar for Firefox
      }}
    >
      {messages.map((message, index) => (
        <FadeInBox display="flex" alignItems="flex-start" key={index} index={index}>
          {message.type === 'text' && <ChatBubbleOutlineIcon fontSize="small" style={{ marginTop: '4px', marginRight: '8px', color: '#015C94' }} />}
          <Typography variant="body1" style={{ whiteSpace: 'pre-line' }}>
            <strong>{message.sender}:</strong> {message.content}
          </Typography>
        </FadeInBox>
      ))}
    </Stack>
  );
};

export default ChatHistory;
