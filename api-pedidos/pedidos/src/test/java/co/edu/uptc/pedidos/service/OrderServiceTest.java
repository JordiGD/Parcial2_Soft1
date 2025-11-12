package co.edu.uptc.pedidos.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.MongoDBContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import co.edu.uptc.pedidos.client.DrinkApiClient;
import co.edu.uptc.pedidos.entity.Order;
import co.edu.uptc.pedidos.model.Drink;
import co.edu.uptc.pedidos.model.OrderDTO;
import co.edu.uptc.pedidos.model.OrderItem;
import co.edu.uptc.pedidos.repo.OrderRepo;

@Testcontainers
@ExtendWith(MockitoExtension.class)
@SpringBootTest
class OrderServiceTest {
    
    @Container
    static MongoDBContainer mongoDBContainer = new MongoDBContainer("mongo:7.0")
            .withExposedPorts(27017);
    
    @DynamicPropertySource
    static void setProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.data.mongodb.uri", mongoDBContainer::getReplicaSetUrl);
    }
    
    @Mock
    private DrinkApiClient drinkApiClient;
    
    @Mock
    private OrderRepo orderRepo;
    
    @Mock 
    private SequenceGenerator sequenceGenerator;
    
    private OrderService orderService;
    
    @BeforeEach
    void setUp() {
        orderService = new OrderService(drinkApiClient, orderRepo, sequenceGenerator);
    }
    
    @Test
    @DisplayName("Crear pedido exitoso cuando bebida existe")
    void testCreateOrderSuccess() {
        Drink drink = new Drink(1L, "Latte", "medium", 3.50);
        OrderDTO orderDTO = new OrderDTO();
        OrderItem item = new OrderItem();
        item.setDrink(drink);
        item.setSize("medium");
        item.setQuantity(1);
        orderDTO.setItems(List.of(item));
        
        Order savedOrder = new Order();
        savedOrder.setId(1001L);
        savedOrder.setStatus("CONFIRMED");
        savedOrder.setTotalPrice(3.50);
        
        when(drinkApiClient.getDrinkByName("Latte")).thenReturn(drink);
        when(sequenceGenerator.generateNextOrderId()).thenReturn(1001L);
        when(orderRepo.save(any(Order.class))).thenReturn(savedOrder);
        
        OrderDTO result = orderService.createOrder(orderDTO);
        
        assertNotNull(result.getId());
        assertEquals("CONFIRMED", result.getStatus());
        assertEquals(3.50, result.getTotalPrice());
        verify(drinkApiClient, times(1)).getDrinkByName("Latte");
        verify(sequenceGenerator, times(1)).generateNextOrderId();
        verify(orderRepo, times(1)).save(any(Order.class));
    }
    
    @Test
    @DisplayName("Rechazar pedido cuando bebida no existe")
    void testCreateOrderDrinkNotFound() {
        OrderDTO orderDTO = new OrderDTO();
        OrderItem item = new OrderItem();
        item.setDrink(new Drink(1L, "Inexistente", "small", 0.0));
        item.setSize("small");
        item.setQuantity(1);
        orderDTO.setItems(List.of(item));
        
        when(drinkApiClient.getDrinkByName("Inexistente")).thenReturn(null);
        
        assertThrows(IllegalArgumentException.class, () -> {
            orderService.createOrder(orderDTO);
        });
        
        verify(drinkApiClient, times(1)).getDrinkByName("Inexistente");
    }
    
    @Test
    @DisplayName("Rechazar pedido cuando tamaño no coincide")
    void testCreateOrderWrongSize() {
        Drink drink = new Drink(1L, "Espresso", "small", 2.00);
        OrderDTO orderDTO = new OrderDTO();
        OrderItem item = new OrderItem();
        item.setDrink(new Drink(1L, "Espresso", "large", 2.00));
        item.setSize("large");
        item.setQuantity(1);
        orderDTO.setItems(List.of(item));
        
        when(drinkApiClient.getDrinkByName("Espresso")).thenReturn(drink);
        
        assertThrows(IllegalArgumentException.class, () -> {
            orderService.createOrder(orderDTO);
        });
    }
    
    @Test
    @DisplayName("Obtener todos los pedidos")
    void testGetAllOrders() {
        Drink drink = new Drink(1L, "Americano", "medium", 2.50);
        when(drinkApiClient.getDrinkByName("Americano")).thenReturn(drink);
        when(sequenceGenerator.generateNextOrderId()).thenReturn(1001L, 1002L);
        
        Order savedOrder1 = new Order();
        savedOrder1.setId(1001L);
        savedOrder1.setStatus("CONFIRMED");
        savedOrder1.setTotalPrice(2.50);
        
        Order savedOrder2 = new Order();
        savedOrder2.setId(1002L);
        savedOrder2.setStatus("CONFIRMED");
        savedOrder2.setTotalPrice(2.50);
        
        when(orderRepo.save(any(Order.class))).thenReturn(savedOrder1, savedOrder2);
        when(orderRepo.findAll()).thenReturn(List.of(savedOrder1, savedOrder2));
        
        OrderDTO orderDTO1 = new OrderDTO();
        OrderItem item1 = new OrderItem();
        item1.setDrink(drink);
        item1.setSize("medium");
        item1.setQuantity(1);
        orderDTO1.setItems(List.of(item1));
        
        OrderDTO orderDTO2 = new OrderDTO();
        OrderItem item2 = new OrderItem();
        item2.setDrink(drink);
        item2.setSize("medium");
        item2.setQuantity(1);
        orderDTO2.setItems(List.of(item2));
        
        orderService.createOrder(orderDTO1);
        orderService.createOrder(orderDTO2);
        
        var orders = orderService.getAllOrders();
        
        assertEquals(2, orders.size());
    }

}
