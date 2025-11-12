import { render, screen } from '@testing-library/react';
import App from './App';

test('renders VirtualCoffee app', () => {
  render(<App />);
  const headerElement = screen.getByText('VirtualCoffee - Pedidos');
  expect(headerElement).toBeInTheDocument();
});

test('renders order form and history components', () => {
  render(<App />);
  expect(screen.getByTestId('order-form')).toBeInTheDocument();
  expect(screen.getByText('Cargando historial...')).toBeInTheDocument();
});
