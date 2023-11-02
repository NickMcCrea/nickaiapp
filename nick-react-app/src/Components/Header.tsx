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
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';
import Box from '@mui/material/Box';

interface HeaderProps {
  estimatedCost?: string;
  selectedModel: string;  // New prop
  onModelChange: (model: string) => void;  // New prop
}

const StyledAppBar = styled(AppBar)({
  backgroundColor: '#015C94',
});

const StyledToolbar = styled(Toolbar)({
  padding: '0 2rem',
});

const Title = styled(Typography)({
  flexGrow: 0,
  color: '#C9E0F5',
  fontFamily: '"Trade Gothic", Arial, sans-serif',
  marginRight: '2rem',
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




const Header: React.FC<HeaderProps> = ({ estimatedCost, selectedModel, onModelChange }) => {
 
  const [state, setState] = React.useState({
    checkedGPT: true,
  });

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newCheckedState = event.target.checked;
    setState({ ...state, [event.target.name]: newCheckedState });
    onModelChange(newCheckedState ? 'GPT3.5' : 'GPT4'); // Call onModelChange to update model in App.tsx
  };

  return (
    <StyledAppBar position="static">
      <StyledToolbar>
        <StyledIconButton edge="start">
          <DataThresholdingIcon fontSize="large" />
        </StyledIconButton>
        <Title variant="h5">
          <i>Talk To Your Data</i>
        
        </Title>

         {/* Added Switch */}
         <FormControlLabel
          control={
            <Switch
              checked={state.checkedGPT}
              onChange={handleChange}
              name="checkedGPT"
              sx={{
                '& .MuiSwitch-thumb': {
                  backgroundColor: '#187ABA', // Morgan Stanley blue when unchecked
                },
                '& .MuiSwitch-switchBase.Mui-checked': {
                  color: '#A3CAE3', // Morgan Stanley green when checked
                },
                '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
                  backgroundColor: '#335574', // Morgan Stanley green when checked
                },
              }}
            />
          }
          label={state.checkedGPT ? 'GPT3.5' : 'GPT4'}
        />


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
