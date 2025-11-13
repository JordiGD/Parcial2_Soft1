Reflexión del Proyecto – VirtualCoffee
Lecciones aprendidas

Durante el desarrollo del sistema VirtualCoffee aprendimos la importancia de integrar diferentes lenguajes y frameworks dentro de un entorno de pruebas completo y controlado. Aplicar TDD (Test Driven Development) tanto en Python con pytest como en Java con JUnit 5 nos permitió entender cómo los casos de prueba pueden guiar el diseño del código y reducir errores desde etapas tempranas del desarrollo.

Comprendimos también el valor del uso de mocks con Mockito y FastAPI TestClient para simular dependencias externas sin necesidad de ejecutar todos los servicios al mismo tiempo. Esto facilitó las pruebas de integración entre la API de bebidas y la API de pedidos.

Las pruebas E2E con Selenium nos enseñaron la importancia de automatizar los flujos completos desde las interfaces web (Angular y React), garantizando coherencia entre el backend y el frontend.
Por último, el análisis estático con SonarQube, pylint y mypy nos permitió identificar errores comunes, duplicación de código y áreas de mejora en la mantenibilidad del proyecto.

Mejores prácticas aplicadas

Desarrollo guiado por pruebas (TDD): priorizamos la creación de pruebas antes de implementar la lógica de negocio.

Uso de mocks y stubs: simulamos la API de bebidas en las pruebas de pedidos para mantener independencia entre los componentes.

Automatización de pruebas E2E: empleamos Selenium para validar la experiencia del usuario y la integración total del sistema.

Validaciones de entrada robustas: implementamos reglas en los endpoints (/menu y /orders) para evitar datos inconsistentes.

Análisis estático continuo: utilizamos herramientas como SonarQube y pylint para detectar code smells y errores de estilo.

Principios SOLID y separación por capas: en la API de Java mantuvimos una arquitectura clara y mantenible.

Control de versiones (Git): registramos commits frecuentes y descriptivos para garantizar trazabilidad y colaboración.

Principales dificultades

Una de las principales dificultades fue la comunicación entre las dos APIs, especialmente al simular la consulta de disponibilidad de bebidas desde la API de pedidos. Tuvimos que configurar correctamente los mocks y los endpoints para evitar errores de conexión y sincronización.

También encontramos retos en la configuración de SonarQube, ya que fue necesario ajustar reportes de cobertura y resolver advertencias que no siempre eran evidentes.
Durante las pruebas E2E, el manejo de los tiempos de espera (waits) y la sincronización entre Angular y React resultó complejo, especialmente al automatizar flujos que dependían de datos generados en tiempo real.
Finalmente, integrar herramientas como pytest, JUnit, Selenium y los dos frontends en un mismo flujo de pruebas implicó coordinar múltiples entornos y dependencias de forma precisa.