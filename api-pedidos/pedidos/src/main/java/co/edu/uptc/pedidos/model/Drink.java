package co.edu.uptc.pedidos.model;

public class Drink {
    private Long id;
    private String name;
    private String size;
    private Double price;

    public Drink() {}
    
    public Drink(Long id, String name, String size, Double price) {
        this.id = id;
        this.name = name;
        this.size = size;
        this.price = price;
    }
    
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getSize() { return size; }
    public void setSize(String size) { this.size = size; }
    public Double getPrice() { return price; }
    public void setPrice(Double price) { this.price = price; }
}
