package co.edu.uptc.pedidos.exception;

public class OrderProcessingException extends RuntimeException {
    
    public OrderProcessingException(String message) {
        super(message);
    }
    
    public OrderProcessingException(String message, Throwable cause) {
        super(message, cause);
    }
}