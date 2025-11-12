package co.edu.uptc.pedidos.steps;

import io.cucumber.java.en.*;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import io.cucumber.java.Before;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import co.edu.uptc.pedidos.client.DrinkApiClient;
import co.edu.uptc.pedidos.entity.Order;
import co.edu.uptc.pedidos.model.Drink;
import co.edu.uptc.pedidos.model.OrderDTO;
import co.edu.uptc.pedidos.model.OrderItem;
import co.edu.uptc.pedidos.repo.OrderRepo;
import co.edu.uptc.pedidos.service.OrderService;
import co.edu.uptc.pedidos.service.SequenceGenerator;

import java.util.List;

public class OrderSteps {
    
    @Mock
    private DrinkApiClient drinkApiClient;
    
    @Mock
    private OrderRepo orderRepo;
    
    @Mock
    private SequenceGenerator sequenceGenerator;
    
    private OrderService orderService;
    
    private OrderDTO currentOrder;
    private Exception thrownException;

    @Before
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        orderService = new OrderService(drinkApiClient, orderRepo, sequenceGenerator);
    }

    @Given("the drink API is available")
    public void theDrinkAPIIsAvailable() {
        
    }

    @Given("a drink {string} with size {string} and price {double} exists")
    public void aDrinkExists(String name, String size, Double price) {
        Drink drink = new Drink(1L, name, size, price);
        when(drinkApiClient.getDrinkByName(name)).thenReturn(drink);
    }

    @When("I create an order for {string} with size {string}")
    public void iCreateAnOrder(String drinkName, String size) {
        try {
            currentOrder = new OrderDTO();
            OrderItem item = new OrderItem();
            Drink drink = new Drink(1L, drinkName, size, 0.0);
            item.setDrink(drink);
            item.setSize(size);
            item.setQuantity(1);
            currentOrder.setItems(List.of(item));
            
            Drink mockedDrink = drinkApiClient.getDrinkByName(drinkName);
            when(sequenceGenerator.generateNextOrderId()).thenReturn(1001L);
            Order savedOrder = new Order();
            savedOrder.setId(1001L);
            savedOrder.setStatus("CONFIRMED");
            if (mockedDrink != null) {
                savedOrder.setTotalPrice(mockedDrink.getPrice() * item.getQuantity());
            }
            when(orderRepo.save(any(Order.class))).thenReturn(savedOrder);
            
            currentOrder = orderService.createOrder(currentOrder);
        } catch (Exception e) {
            thrownException = e;
        }
    }

    @Then("the order should be confirmed")
    public void theOrderShouldBeConfirmed() {
        assertNotNull(currentOrder);
        assertEquals("CONFIRMED", currentOrder.getStatus());
    }

    @Then("the order price should be {double}")
    public void theOrderPriceShouldBe(Double price) {
        assertEquals(price, currentOrder.getTotalPrice());
    }

    @Then("the order status should be {string}")
    public void theOrderStatusShouldBe(String status) {
        assertEquals(status, currentOrder.getStatus());
    }

    @Then("the order should be rejected")
    public void theOrderShouldBeRejected() {
        assertNotNull(thrownException);
        assertTrue(thrownException instanceof IllegalArgumentException);
    }

    @Then("I should see error {string}")
    public void iShouldSeeError(String errorMessage) {
        assertTrue(thrownException.getMessage().contains(errorMessage));
    }
}
