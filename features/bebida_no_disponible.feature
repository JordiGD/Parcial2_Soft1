# language: es
Característica: Rechazar pedido de bebida no disponible
  Como sistema de VirtualCoffee
  Quiero rechazar pedidos de bebidas no disponibles
  Para mantener la integridad del sistema

  Antecedentes:
    Dado que la API de bebidas está disponible
    Y NO existe una bebida llamada "SuperCafe"

  Escenario: Rechazar pedido de bebida inexistente
    Dado que estoy en la página de pedidos
    Cuando intento pedir "SuperCafe" en tamaño "medium"
    Entonces el pedido debe ser rechazado
    Y debo ver el mensaje de error "Bebida no disponible en el menú"
    Y el pedido debe tener estado "REJECTED"
    Y el precio debe ser 0.00

  Escenario: Rechazar pedido con tamaño no disponible
    Dado que existe una bebida "Latte" solo en tamaño "small"
    Cuando intento pedir "Latte" en tamaño "large"
    Entonces el pedido debe ser rechazado
    Y debo ver "La bebida no está disponible en el tamaño solicitado"

  Escenario: Validación de campos obligatorios
    Dado que estoy en la página de pedidos
    Cuando intento enviar el formulario sin nombre de bebida
    Entonces el botón de envío debe estar deshabilitado
    Y debo ver un mensaje de validación

  Esquema del escenario: Validaciones de entrada
    Cuando intento pedir "<bebida>" en tamaño "<tamaño>"
    Entonces el resultado debe ser "<resultado>"
    Y el mensaje debe contener "<mensaje>"

    Ejemplos:
      | bebida          | tamaño  | resultado | mensaje                    |
      |                 | medium  | INVALID   | nombre no puede estar vacío|
      | Latte           | grande  | INVALID   | Tamaño inválido            |
      | BebidaFalsa     | small   | REJECTED  | no disponible              |