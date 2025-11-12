package co.edu.uptc.pedidos.entity;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import co.edu.uptc.pedidos.model.OrderItem;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@Document(collection = "orders")
public class Order {

    @Id
    private String mongoId; // MongoDB ObjectId
    private Long id; // Business ID for schema validation
    private List<OrderItem> items;
    private Double totalPrice;
    private LocalDateTime orderDate;
    private String status;
    
    public Order(Long id, List<OrderItem> items, Double totalPrice, String status) {
        this.id = id;
        this.items = items;
        this.totalPrice = totalPrice;
        this.status = status;
        this.orderDate = LocalDateTime.now();
    }
    
    public Order(String mongoId, Long id, List<OrderItem> items, Double totalPrice, LocalDateTime orderDate, String status) {
        this.mongoId = mongoId;
        this.id = id;
        this.items = items;
        this.totalPrice = totalPrice;
        this.orderDate = orderDate;
        this.status = status;
    }
}
