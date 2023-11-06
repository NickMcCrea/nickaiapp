import React from 'react';
import { Stack, Typography, Box } from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import ComputerIcon from '@mui/icons-material/Computer';
import { styled, keyframes } from '@mui/system';
import SettingsIcon from '@mui/icons-material/Settings'; // Import the gear icon


// Add a styled component for messages from "Working"
const WorkingMessage = styled(Typography)({
  border: '1px solid #b0bec5', // light grey border
  borderRadius: '4px', // rounded corners
  backgroundColor: '#e3f2fd', // light blue background
  padding: '2px', // padding inside the border
});

const FadeInBox = styled(Box)<{ index?: number }>(({ index = 0 }) => ({
  opacity: 0,
  transform: 'translateY(10px)',
  animation: 'fadein 0.05s forwards',
  animationDelay: `${0.05 * (index)}s`,
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
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
`;

const AnimatedComputerIcon = styled(ComputerIcon)({
  animation: `${pulseAnimation} 1s infinite`,
  
});

export interface Message {
  type: 'text' | 'jsx';
  content: string | JSX.Element;
  timestamp: Date;
  sender: string;
}

interface ChatHistoryProps {
  messages: Message[];
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages }) => {

  const lastMessageIsFromHuman = !!messages.length && messages[messages.length - 1].sender != 'Assistant';

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
          {message.sender === 'You' ? (
          <PersonIcon fontSize="small" style={{ marginTop: '4px', marginRight: '8px', color: '#015C94' }} />
        ) : message.sender === 'Working' ? ( // Check if the sender is 'Working'
          <SettingsIcon fontSize="small" style={{ marginTop: '4px', marginRight: '8px', color: '#015C94' }} /> // Use the gear icon for 'Working'
        ) : (
          <ComputerIcon fontSize="small" style={{ marginTop: '4px', marginRight: '8px', color: '#015C94' }} />
        )}

        {message.sender === 'Working' ? (
          <WorkingMessage variant="body1" align='left'>
            {message.content}
          </WorkingMessage>
        ) : (
          <Typography variant="body1" style={{ whiteSpace: 'pre-line' }} align='left'>
            {message.content}
          </Typography>
        )}
      </FadeInBox>
      ))}
      {lastMessageIsFromHuman && <AnimatedComputerIcon fontSize="small" style={{  marginRight: '8px', color: '#015C94', alignSelf: 'flex-start' }} />}
    </Stack>
  );
};

export default ChatHistory;