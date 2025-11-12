package co.edu.uptc.pedidos.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

import co.edu.uptc.pedidos.entity.Order;
import co.edu.uptc.pedidos.model.OrderDTO;

@Mapper
public interface OrderMapper {

    OrderMapper INSTANCE = Mappers.getMapper(OrderMapper.class);

    @Mapping(target = "mongoId", ignore = true) // MongoDB will generate this
    Order toEntity(OrderDTO orderDTO);
    
    OrderDTO toDTO(Order order);
    
}
