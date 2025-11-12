import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

class TestCompleteFlow:
    """Prueba del flujo completo: Agregar bebida y hacer pedido"""
    
    @pytest.fixture(scope="class")
    def driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        
        yield driver
        driver.quit()
    
    def test_flujo_completo_agregar_y_pedir(self, driver):
        """
        Flujo completo E2E:
        1. Agregar nueva bebida en Angular
        2. Verificar que aparece en el menú
        3. Hacer pedido en React
        4. Verificar que aparece en historial
        """
        bebida_nombre = f"Mocha Test {int(time.time())}"
        
        driver.get("http://localhost:4200")
        wait = WebDriverWait(driver, 15)
        
        name_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='input-name']"))
        )
        name_input.clear()
        name_input.send_keys(bebida_nombre)
        
        size_select = driver.find_element(By.CSS_SELECTOR, "[data-testid='select-size']")
        size_select.send_keys("medium")
        
        price_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='input-price']")
        price_input.clear()
        price_input.send_keys("5.00")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='btn-submit']")
        submit_btn.click()
        
        success_msg = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "exitosamente" in success_msg.text.lower()
        
        driver.save_screenshot("screenshots/1_bebida_agregada.png")
        time.sleep(2)
        
        menu_table = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "menu-table"))
        )
        assert bebida_nombre in menu_table.text
        
        driver.save_screenshot("screenshots/2_bebida_en_menu.png")
        
        driver.get("http://localhost:3000")
        
        drink_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='input-drink-name']"))
        )
        drink_input.clear()
        drink_input.send_keys(bebida_nombre)
        
        size_select = driver.find_element(By.CSS_SELECTOR, "[data-testid='select-size']")
        size_select.send_keys("medium")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='btn-submit']")
        submit_btn.click()
        
        success_msg = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='success-message']"))
        )
        
        driver.save_screenshot("screenshots/3_pedido_realizado.png")
        time.sleep(2)
        
        orders_table = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='orders-table']"))
        )
        assert bebida_nombre in orders_table.text
        assert "CONFIRMED" in orders_table.text
        
        driver.save_screenshot("screenshots/4_pedido_en_historial.png")
        
        print(f"\nFlujo completo exitoso para: {bebida_nombre}")