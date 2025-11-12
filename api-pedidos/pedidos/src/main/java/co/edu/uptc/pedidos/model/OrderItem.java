package co.edu.uptc.pedidos.model;

import jakarta.validation.constraints.Pattern;

public class OrderItem{

    private Long id;
    private String productName;
    private Integer quantity;
    private Double price;
    private Drink drink;
    @Pattern(regexp = "small|medium|large", message = "El tamaño debe ser small, medium o large")
    private String size;

    public OrderItem() {}

    public OrderItem(Long id, String productName, Integer quantity, Double price, Drink drink, String size) {
        this.id = id;
        this.productName = productName;
        this.quantity = quantity;
        this.price = price;
        this.drink = drink;
        this.size = size;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }
    public Integer getQuantity() { return quantity; }
    public void setQuantity(Integer quantity) { this.quantity = quantity; }
    public Double getPrice() { return price; }
    public void setPrice(Double price) { this.price = price; }
    public Drink getDrink() { return drink; }
    public void setDrink(Drink drink) { this.drink = drink; }
    public String getSize() { return size; }
    public void setSize(String size) { this.size = size; }

}