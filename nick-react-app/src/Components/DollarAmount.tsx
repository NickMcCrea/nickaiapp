import React, { useEffect } from 'react';
import { useSpring, animated } from '@react-spring/web';
import { Typography } from '@mui/material';

interface DollarAmountProps {
  amount: number;
}

const DollarAmount: React.FC<DollarAmountProps> = ({ amount }) => {
  const [props, set] = useSpring(() => ({ amount: 0 }));

  useEffect(() => {
    set({ amount });
  }, [amount, set]);

  return (
    <Typography variant="h6">
      <animated.span>
        {props.amount.to(n => `$${n.toFixed(2)}`)}
      </animated.span>
    </Typography>
  );
};

export default DollarAmount;
