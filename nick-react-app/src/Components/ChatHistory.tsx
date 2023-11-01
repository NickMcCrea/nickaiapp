import { Stack, Typography, Box } from '@mui/material';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import PersonIcon from '@mui/icons-material/Person';
import ComputerIcon from '@mui/icons-material/Computer';
import React from 'react';
import { styled, keyframes } from '@mui/system';

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

const pulseAnimation = keyframes`
  0% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.5;
  }
`;

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
          {message.type === 'text' && (
            <>
              {message.sender === 'You' ? (
                <PersonIcon fontSize="small" style={{ marginTop: '4px', marginRight: '8px', color: '#015C94' }}
              />) : (
                <ComputerIcon fontSize="small" style={{ marginTop: '4px', marginRight: '8px', color: '#015C94' }}
              />
              )}
            </>
          )}
          <Typography variant="body1" style={{ whiteSpace: 'pre-line' }} align='left'>
           {message.content}
          </Typography>
        </FadeInBox>
      ))}
    </Stack>
  );
};

export default ChatHistory;
