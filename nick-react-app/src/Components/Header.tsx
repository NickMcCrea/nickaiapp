import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import DataThresholdingIcon from '@mui/icons-material/DataThresholding';
import SlideshowIcon from '@mui/icons-material/Slideshow';
import AddBoxIcon from '@mui/icons-material/AddBox'; // Import the new icon
import { styled } from '@mui/system';

interface HeaderProps {
  estimatedCost?: string;
}

const StyledAppBar = styled(AppBar)({
  backgroundColor: '#015C94',
});

const StyledToolbar = styled(Toolbar)({
  padding: '0 2rem',
});

const Title = styled(Typography)({
  flexGrow: 1,
  color: '#C9E0F5',
  fontFamily: '"Trade Gothic", Arial, sans-serif'
});

const StyledIconButton = styled(IconButton)({
  marginRight: '1rem',
  color: '#C9E0F5',
});

const StyledButton = styled(Button)({
  color: '#C9E0F5', // Match the color scheme
});

const EstimatedCost = styled(Typography)({
  fontSize: '0.8rem',
  position: 'absolute',
  right: '2rem',
  top: '50%',
  transform: 'translateY(-50%)'
});




const Header: React.FC<HeaderProps> = ({ estimatedCost }) => {
 

  return (
    <StyledAppBar position="static">
      <StyledToolbar>
        <StyledIconButton edge="start">
          <DataThresholdingIcon fontSize="large" />
        </StyledIconButton>
        <Title variant="h5">
          <i>NickAI</i>
        
        </Title>
        {estimatedCost && (
          <EstimatedCost variant="body2">
            Estimated Cost: {estimatedCost}
          </EstimatedCost>
        )}
  
      </StyledToolbar>
    </StyledAppBar>
  );
};

export default Header;
