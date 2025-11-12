# language: es
Característica: Realizar pedido exitoso
  Como cliente de VirtualCoffee
  Quiero realizar un pedido de una bebida disponible
  Para poder disfrutar de mi bebida favorita

  Antecedentes:
    Dado que la API de bebidas está disponible
    Y existe una bebida "Latte" en tamaño "medium" con precio 3.50

  Escenario: Pedido exitoso de bebida disponible
    Dado que estoy en la página de pedidos
    Cuando selecciono la bebida "Latte"
    Y selecciono el tamaño "medium"
    Y hago clic en "Realizar Pedido"
    Entonces el pedido debe ser creado exitosamente
    Y debo ver el mensaje "Pedido realizado exitosamente"
    Y el pedido debe aparecer en el historial con estado "CONFIRMED"
    Y el precio del pedido debe ser 3.50

  Escenario: Pedido con bebida y tamaño específico
    Dado que estoy en la página de pedidos
    Cuando intento pedir "Espresso" en tamaño "small"
    Entonces si la bebida existe en ese tamaño
    Entonces el pedido debe ser confirmado
    Y el historial debe actualizarse automáticamente

  Esquema del escenario: Pedidos de diferentes bebidas
    Dado que existe una bebida "<bebida>" en tamaño "<tamaño>"
    Cuando hago un pedido de "<bebida>" en tamaño "<tamaño>"
    Entonces el pedido debe tener estado "<estado>"
    Y el precio debe ser "<precio>"

    Ejemplos:
      | bebida      | tamaño | estado    | precio |
      | Cappuccino  | large  | CONFIRMED | 4.00   |
      | Americano   | medium | CONFIRMED | 2.50   |
      | Mocha       | small  | CONFIRMED | 3.00   |