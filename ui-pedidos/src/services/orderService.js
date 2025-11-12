import axios from 'axios';

const API_URL = 'http://localhost:8081/orders';

export const orderService = {
  createOrder: async (orderData) => {
    try {
      const response = await axios.post(API_URL, orderData);
      return response.data;
    } catch (error) {
      throw error.response?.data?.message || 'Error al crear pedido';
    }
  },

  getAllOrders: async () => {
    try {
      const response = await axios.get(API_URL);
      return response.data;
    } catch (error) {
      throw error.response?.data?.message || 'Error al obtener pedidos';
    }
  }
};