import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import InputWithSendButton from './InputWithSendButton';

describe('InputWithSendButton', () => {
  it('calls onSubmit with the input value when send button is clicked', () => {
    const mockOnSubmit = jest.fn();
    const { getByRole, getByLabelText } = render(<InputWithSendButton onSubmit={mockOnSubmit} />);

    const input = getByLabelText(/input/i);
    const sendButton = getByRole('button', { name: /send/i });

    fireEvent.change(input, { target: { value: 'test message' } });
    fireEvent.click(sendButton);

    expect(mockOnSubmit).toHaveBeenCalledWith('test message');
  });
});
