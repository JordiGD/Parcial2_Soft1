package co.edu.uptc.pedidos.service;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.stereotype.Service;

import co.edu.uptc.pedidos.client.DrinkApiClient;
import co.edu.uptc.pedidos.entity.Order;
import co.edu.uptc.pedidos.exception.OrderProcessingException;
import co.edu.uptc.pedidos.mapper.OrderMapper;
import co.edu.uptc.pedidos.model.Drink;
import co.edu.uptc.pedidos.model.OrderDTO;
import co.edu.uptc.pedidos.model.OrderItem;
import co.edu.uptc.pedidos.repo.OrderRepo;

@Service
public class OrderService {

    private final DrinkApiClient drinkApiClient;
    private final OrderRepo orderRepo;
    private final SequenceGenerator sequenceGenerator;
    
    public OrderService(DrinkApiClient drinkApiClient, OrderRepo orderRepo, SequenceGenerator sequenceGenerator) {
        this.drinkApiClient = drinkApiClient;
        this.orderRepo = orderRepo;
        this.sequenceGenerator = sequenceGenerator;
    }
    
    public OrderDTO createOrder(OrderDTO orderDto) {
        System.out.println("=== INICIO createOrder ===");
        System.out.println("OrderDTO recibido - Items: " + (orderDto.getItems() != null ? orderDto.getItems().size() : "null"));
        try {
            if (orderDto.getItems() == null || orderDto.getItems().isEmpty()) {
                throw new IllegalArgumentException("La orden debe tener al menos un item");
            }
            
            double totalPrice = 0.0;
            
            for (OrderItem item : orderDto.getItems()) {
                if (item.getQuantity() <= 0) {
                    throw new IllegalArgumentException("La cantidad debe ser mayor a 0");
                }
                
                String drinkName = item.getDrink() != null ? item.getDrink().getName() : item.getProductName();
                
                if (drinkName == null || drinkName.trim().isEmpty()) {
                    throw new IllegalArgumentException("El nombre de la bebida es requerido");
                }
                
                Drink drink = drinkApiClient.getDrinkByName(drinkName);
            
                if (drink == null) {
                    orderDto.setStatus("REJECTED");
                    orderDto.setTotalPrice(0.0);
                    throw new IllegalArgumentException("Bebida no disponible en el menú: " + drinkName);
                }
                
                if (!drink.getSize().equals(item.getSize())) {
                    orderDto.setStatus("REJECTED");
                    throw new IllegalArgumentException(
                        "La bebida '" + drink.getName() + "' no está disponible en el tamaño '" + item.getSize() + "'"
                    );
                }
                
                totalPrice += drink.getPrice() * item.getQuantity();
            }
            
            Long orderId = sequenceGenerator.generateNextOrderId();
            
            orderDto.setId(orderId);
            orderDto.setTotalPrice(totalPrice);
            orderDto.setStatus("CONFIRMED");
            orderDto.setOrderDate(LocalDateTime.now());
            
            // Debug logging
            System.out.println("OrderDTO before mapping - ID: " + orderDto.getId() + ", OrderDate: " + orderDto.getOrderDate());
            
            Order orderEntity = OrderMapper.INSTANCE.toEntity(orderDto);
            
            // Debug logging
            System.out.println("Order Entity after mapping - ID: " + orderEntity.getId() + ", OrderDate: " + orderEntity.getOrderDate());
            
            Order savedOrder = orderRepo.save(orderEntity);
            
            return OrderMapper.INSTANCE.toDTO(savedOrder);
            
        } catch (IllegalArgumentException e) {
            throw e;
        } catch (Exception e) {
            orderDto.setStatus("ERROR");
            throw new OrderProcessingException("Error al procesar la orden: " + e.getMessage(), e);
        }
    }
    
    public List<OrderDTO> getAllOrders() {
        return orderRepo.findAll()
            .stream()
            .map(OrderMapper.INSTANCE::toDTO)
            .toList();
    }
}
