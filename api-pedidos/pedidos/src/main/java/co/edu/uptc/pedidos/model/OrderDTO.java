package co.edu.uptc.pedidos.model;

import java.time.LocalDateTime;
import java.util.List;

public class OrderDTO {

    private Long id;
    private List<OrderItem> items;
    private Double totalPrice;
    private LocalDateTime orderDate;
    private String status;

    public OrderDTO() {
    }

    public OrderDTO(Long id, List<OrderItem> items, Double totalPrice, LocalDateTime orderDate, String status) {
        this.id = id;
        this.items = items;
        this.totalPrice = totalPrice;
        this.orderDate = orderDate;
        this.status = status;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public List<OrderItem> getItems() {
        return items;
    }

    public void setItems(List<OrderItem> items) {
        this.items = items;
    }

    public Double getTotalPrice() {
        return totalPrice;
    }

    public void setTotalPrice(Double totalPrice) {
        this.totalPrice = totalPrice;
    }

    public LocalDateTime getOrderDate() {
        return orderDate;
    }

    public void setOrderDate(LocalDateTime orderDate) {
        this.orderDate = orderDate;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
