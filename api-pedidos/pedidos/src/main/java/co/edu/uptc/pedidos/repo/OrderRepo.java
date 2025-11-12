package co.edu.uptc.pedidos.repo;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import co.edu.uptc.pedidos.entity.Order;

@Repository
public interface OrderRepo extends MongoRepository<Order, Long> {
    
}
