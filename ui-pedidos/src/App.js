import React, { useState } from 'react';
import OrderForm from './components/OrderForm';
import OrderHistory from './components/OrderHistory';
import './App.css';

function App() {
  const [refreshCounter, setRefreshCounter] = useState(0);

  const handleOrderCreated = () => {
    setRefreshCounter(prev => prev + 1);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>VirtualCoffee - Pedidos</h1>
      </header>
      
      <div className="container">
        <div className="row">
          <div className="col">
            <OrderForm onOrderCreated={handleOrderCreated} />
          </div>
          <div className="col">
            <OrderHistory refresh={refreshCounter} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;