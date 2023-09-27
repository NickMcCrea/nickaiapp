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
import DollarAmount from './DollarAmount';
import { useDollarAmount } from './DollarAmount';  

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

const Header = () => {
 
const context = useDollarAmount();
if (!context) {
    throw new Error("useDollarAmount must be used within a DollarAmountProvider");
}
const { amount, setAmount } = context;

  return (
    <StyledAppBar position="static">
      <StyledToolbar>
        <StyledIconButton edge="start">
          <DataThresholdingIcon fontSize="large" />
        </StyledIconButton>
        <Title variant="h5">
          <i>NickAI</i>
        </Title>
        <DollarAmount amount={amount} />
      </StyledToolbar>
    </StyledAppBar>
  );
};

export default Header;
