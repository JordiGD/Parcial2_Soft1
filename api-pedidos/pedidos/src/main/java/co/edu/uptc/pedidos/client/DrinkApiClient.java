package co.edu.uptc.pedidos.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import co.edu.uptc.pedidos.model.Drink;

@Component
public class DrinkApiClient {
    
    private final RestTemplate restTemplate;
    private final String drinkApiUrl;
    
    public DrinkApiClient(RestTemplate restTemplate,
                         @Value("${drink.api.url}") String drinkApiUrl) {
        this.restTemplate = restTemplate;
        this.drinkApiUrl = drinkApiUrl;
    }
    
    public Drink getDrinkByName(String name) {
        try {
            String url = drinkApiUrl + "/menu/" + name;
            return restTemplate.getForObject(url, Drink.class);
        } catch (HttpClientErrorException.NotFound e) {
            return null;
        }
    }
    
    public boolean isDrinkAvailable(String name, String size) {
        Drink drink = getDrinkByName(name);
        return drink != null && drink.getSize().equals(size);
    }

}
