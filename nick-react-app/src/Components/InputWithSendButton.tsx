import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import SendIcon from '@mui/icons-material/Send';

interface Props {
  onSubmit: (value: string) => void;
}

const InputWithSendButton: React.FC<Props> = ({ onSubmit }) => {
  const [value, setValue] = useState('');

  const handleSubmit = () => {
    onSubmit(value);
    setValue('');
  };

  return (
    <div style={{ display: 'flex', alignItems: 'flex-end' }}>
      <TextField
        fullWidth
        multiline
        variant="outlined"
        value={value}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
          }
        }}
        onChange={(e) => setValue(e.target.value)}
      />
      <IconButton color="primary" onClick={handleSubmit}>
        <SendIcon />
      </IconButton>
    </div>
  );
};

export default InputWithSendButton;
