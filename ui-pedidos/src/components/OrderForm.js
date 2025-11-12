import React, { useState } from 'react';
import { orderService } from '../services/orderService';
import './OrderForm.css';

function OrderForm({ onOrderCreated }) {
  const [orderItems, setOrderItems] = useState([{
    id: 1,
    productName: '',
    size: 'medium',
    quantity: 1
  }]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleItemChange = (index, field, value) => {
    setOrderItems(prev => prev.map((item, i) => 
      i === index ? { ...item, [field]: value } : item
    ));
  };

  const addItem = () => {
    setOrderItems(prev => [...prev, {
      id: Date.now(),
      productName: '',
      size: 'medium',
      quantity: 1
    }]);
  };

  const removeItem = (index) => {
    setOrderItems(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    // Validar que todos los items tengan nombre de producto
    const validItems = orderItems.filter(item => item.productName.trim() !== '');
    if (validItems.length === 0) {
      setError('Debe agregar al menos un producto al pedido');
      setLoading(false);
      return;
    }

    try {
      const orderData = {
        items: validItems.map(item => ({
          productName: item.productName,
          quantity: item.quantity,
          size: item.size
        }))
      };
      
      const order = await orderService.createOrder(orderData);
      setSuccess(true);
      setOrderItems([{
        id: 1,
        productName: '',
        size: 'medium', 
        quantity: 1
      }]);
      if (onOrderCreated) {
        onOrderCreated(order);
      }
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="order-form-container">
      <h2>Realizar Pedido</h2>
      
      {success && (
        <div className="alert alert-success" data-testid="success-message">
          ¡Pedido realizado exitosamente!
        </div>
      )}
      
      {error && (
        <div className="alert alert-error" data-testid="error-message">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} data-testid="order-form">
        <div className="order-items-section">
          <h3>Productos del Pedido</h3>
          
          {orderItems.map((item, index) => (
            <div key={item.id} className="order-item-form">
              <div className="item-header">
                <span className="item-number">Producto {index + 1}</span>
                {orderItems.length > 1 && (
                  <button
                    type="button"
                    className="btn-remove-item"
                    onClick={() => removeItem(index)}
                    data-testid={`btn-remove-${index}`}
                  >
                    ✕
                  </button>
                )}
              </div>
              
              <div className="item-form-grid">
                <div className="form-group">
                  <label htmlFor={`productName-${index}`}>Nombre de la Bebida:</label>
                  <input
                    type="text"
                    id={`productName-${index}`}
                    value={item.productName}
                    onChange={(e) => handleItemChange(index, 'productName', e.target.value)}
                    placeholder="Ej: Latte, Espresso..."
                    data-testid={`input-product-name-${index}`}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor={`quantity-${index}`}>Cantidad:</label>
                  <input
                    type="number"
                    id={`quantity-${index}`}
                    value={item.quantity}
                    onChange={(e) => handleItemChange(index, 'quantity', parseInt(e.target.value))}
                    min="1"
                    max="10"
                    data-testid={`input-quantity-${index}`}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor={`size-${index}`}>Tamaño:</label>
                  <select
                    id={`size-${index}`}
                    value={item.size}
                    onChange={(e) => handleItemChange(index, 'size', e.target.value)}
                    data-testid={`select-size-${index}`}
                  >
                    <option value="small">Pequeño</option>
                    <option value="medium">Mediano</option>
                    <option value="large">Grande</option>
                  </select>
                </div>
              </div>
            </div>
          ))}
          
          <button
            type="button"
            className="btn-add-item"
            onClick={addItem}
            data-testid="btn-add-item"
          >
            ➕ Agregar otro producto
          </button>
        </div>

        <div className="form-actions">
          <button 
            type="submit" 
            disabled={loading || orderItems.every(item => !item.productName.trim())}
            className="btn-submit"
            data-testid="btn-submit"
          >
            {loading ? 'Procesando...' : 'Realizar Pedido'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default OrderForm;