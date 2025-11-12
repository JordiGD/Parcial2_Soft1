import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class TestReactFlow:
    """Pruebas E2E para la interfaz React de pedidos"""
    
    @pytest.fixture(scope="class")
    def driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        
        yield driver
        driver.quit()
    
    def test_realizar_pedido_valido(self, driver):
        """TC03: Realizar pedido válido desde React"""
        driver.get("http://localhost:3000")
        
        wait = WebDriverWait(driver, 10)
        
        drink_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='input-drink-name']"))
        )
        drink_input.clear()
        drink_input.send_keys("Cappuccino E2E")
        
        size_select = driver.find_element(By.CSS_SELECTOR, "[data-testid='select-size']")
        size_select.send_keys("large")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='btn-submit']")
        submit_btn.click()
        
        success_msg = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='success-message']"))
        )
        assert "exitosamente" in success_msg.text.lower()
        
        driver.save_screenshot("screenshots/pedido_realizado.png")
        time.sleep(2)
    
    def test_historial_actualizado(self, driver):
        """TC05: Verificar que el historial se actualiza tras pedido"""
        driver.get("http://localhost:3000")
        
        wait = WebDriverWait(driver, 10)
        
        orders_table = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='orders-table']"))
        )
        
        rows = orders_table.find_elements(By.TAG_NAME, "tr")
        assert len(rows) > 0
        
        driver.save_screenshot("screenshots/historial_pedidos.png")
    
    def test_pedido_bebida_no_existe(self, driver):
        """TC04: Intentar pedir bebida que no existe"""
        driver.get("http://localhost:3000")
        
        wait = WebDriverWait(driver, 10)
        
        drink_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='input-drink-name']"))
        )
        drink_input.clear()
        drink_input.send_keys("BebidaInexistente999")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='btn-submit']")
        submit_btn.click()
        
        error_msg = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='error-message']"))
        )
        assert "no disponible" in error_msg.text.lower() or "error" in error_msg.text.lower()
        
        driver.save_screenshot("screenshots/pedido_rechazado.png")