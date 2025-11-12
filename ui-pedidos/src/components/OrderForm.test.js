import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import OrderForm from './OrderForm';
import { orderService } from '../services/orderService';

jest.mock('../services/orderService');

describe('OrderForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders order form', () => {
    render(<OrderForm />);
    expect(screen.getByRole('heading', { name: 'Realizar Pedido' })).toBeInTheDocument();
    expect(screen.getByTestId('input-product-name-0')).toBeInTheDocument();
    expect(screen.getByTestId('btn-add-item')).toBeInTheDocument();
  });

  test('submits form with valid data', async () => {
    const mockOrder = {
      id: 1,
      drinkName: 'Latte',
      size: 'medium',
      price: 3.50,
      status: 'CONFIRMED'
    };
    
    orderService.createOrder.mockResolvedValue(mockOrder);
    
    render(<OrderForm />);
    
    const drinkInput = screen.getByTestId('input-product-name-0');
    const submitButton = screen.getByTestId('btn-submit');
    
    fireEvent.change(drinkInput, { target: { value: 'Latte' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByTestId('success-message')).toBeInTheDocument();
    });
    
    expect(orderService.createOrder).toHaveBeenCalledWith({
      items: [{
        productName: 'Latte',
        size: 'medium',
        quantity: 1
      }]
    });
  });

  test('shows error when order fails', async () => {
    orderService.createOrder.mockRejectedValue('Bebida no disponible');
    
    render(<OrderForm />);
    
    const drinkInput = screen.getByTestId('input-product-name-0');
    const submitButton = screen.getByTestId('btn-submit');
    
    fireEvent.change(drinkInput, { target: { value: 'NoExiste' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByTestId('error-message')).toBeInTheDocument();
    });
  });

  test('can add multiple items to order', async () => {
    render(<OrderForm />);
    
    // Agregar primer producto
    const firstDrinkInput = screen.getByTestId('input-product-name-0');
    fireEvent.change(firstDrinkInput, { target: { value: 'Latte' } });
    
    // Agregar segundo producto
    const addButton = screen.getByTestId('btn-add-item');
    fireEvent.click(addButton);
    
    const secondDrinkInput = screen.getByTestId('input-product-name-1');
    fireEvent.change(secondDrinkInput, { target: { value: 'Cappuccino' } });
    
    expect(screen.getByDisplayValue('Latte')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Cappuccino')).toBeInTheDocument();
  });

  test('disables submit button when all product names are empty', () => {
    render(<OrderForm />);
    const submitButton = screen.getByTestId('btn-submit');
    expect(submitButton).toBeDisabled();
  });
});