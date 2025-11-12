import React, { useState, useEffect } from 'react';
import { orderService } from '../services/orderService';
import './OrderHistory.css';

function OrderHistory({ refresh }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadOrders = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await orderService.getAllOrders();
      setOrders(data);
    } catch (err) {
      setError('Error al cargar el historial');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOrders();
  }, [refresh]);

  const getStatusBadge = (status) => {
    const statusClasses = {
      'CONFIRMED': 'badge-success',
      'PENDING': 'badge-warning',
      'REJECTED': 'badge-error'
    };
    return statusClasses[status] || 'badge-default';
  };

  if (loading) {
    return <div className="loading">Cargando historial...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="order-history-container">
      <h2>Historial de Pedidos</h2>
      
      {orders.length === 0 ? (
        <p className="empty-message">No hay pedidos registrados</p>
      ) : (
        <div className="orders-container">
          {orders.map((order) => (
            <div key={order.id} className="order-card" data-testid={`order-${order.id}`}>
              <div className="order-header">
                <h3>Pedido #{order.id}</h3>
                <span className={`badge ${getStatusBadge(order.status)}`}>
                  {order.status}
                </span>
              </div>
              
              <div className="order-details">
                <p><strong>Fecha:</strong> {new Date(order.orderDate).toLocaleString()}</p>
                <p><strong>Total:</strong> ${order.totalPrice?.toFixed(2) || '0.00'}</p>
                
                <div className="order-items">
                  <h4>Productos:</h4>
                  {order.items && order.items.length > 0 ? (
                    <ul>
                      {order.items.map((item, index) => (
                        <li key={index} className="order-item">
                          <span className="item-name">{item.productName}</span>
                          <span className="item-details">
                            {item.quantity}x {item.size} - ${item.price?.toFixed(2) || '0.00'}
                          </span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="no-items">Sin productos</p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default OrderHistory;