import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useSpring, animated } from '@react-spring/web';
import { Typography } from '@mui/material';

// Define Context Type
interface DollarAmountContextType {
  amount: number;
  setAmount: React.Dispatch<React.SetStateAction<number>>;
}

// Create Context
export const DollarAmountContext = createContext<DollarAmountContextType | null>(null);

// Custom Hook for using Dollar Amount
export const useDollarAmount = () => {
  return useContext(DollarAmountContext);
};

// Provider Component
interface DollarAmountProviderProps {
  children: ReactNode;
}

export const DollarAmountProvider: React.FC<DollarAmountProviderProps> = ({ children }) => {
  const [amount, setAmount] = useState(0);

  return (
    <DollarAmountContext.Provider value={{ amount, setAmount }}>
      {children}
    </DollarAmountContext.Provider>
  );
};

// DollarAmount Component
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
