Feature: Order Management
  As a customer
  I want to order drinks
  So that I can enjoy my favorite beverages

  Background:
    Given the drink API is available
    And a drink "Latte" with size "medium" and price 3.50 exists

  Scenario: Successfully create an order
    When I create an order for "Latte" with size "medium"
    Then the order should be confirmed
    And the order price should be 3.50
    And the order status should be "CONFIRMED"

  Scenario: Reject order for non-existent drink
    When I create an order for "FakeDrink" with size "small"
    Then the order should be rejected
    And I should see error "Bebida no disponible en el menú"

  Scenario Outline: Order different drinks
    Given a drink "<drink>" with size "<size>" and price <price> exists
    When I create an order for "<drink>" with size "<size>"
    Then the order should be confirmed
    And the order price should be <price>

    Examples:
      | drink      | size   | price |
      | Espresso   | small  | 2.00  |
      | Cappuccino | large  | 4.00  |
      | Americano  | medium | 2.50  |