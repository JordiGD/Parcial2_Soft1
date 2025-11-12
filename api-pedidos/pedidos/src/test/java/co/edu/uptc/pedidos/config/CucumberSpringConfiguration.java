package co.edu.uptc.pedidos.config;

import io.cucumber.spring.CucumberContextConfiguration;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;
import co.edu.uptc.pedidos.PedidosApplication;

@CucumberContextConfiguration
@SpringBootTest(classes = PedidosApplication.class, properties = {"drink.api.url=http://localhost:9999"})
public class CucumberSpringConfiguration {

    @TestConfiguration
    static class TestConfig {
        @Bean
        public RestTemplate testRestTemplate() {
            return new RestTemplate();
        }
    }
}