import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class TestAngularFlow:
    """Pruebas E2E para la interfaz Angular de bebidas"""
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Fixture para el driver de Selenium"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        
        yield driver
        driver.quit()
    
    def test_ver_menu_vacio(self, driver):
        """TC01: Ver menú vacío en Angular"""
        driver.get("http://localhost:4200")
        
        wait = WebDriverWait(driver, 10)
        menu_container = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "menu-container"))
        )
        
        assert "Menú de Bebidas" in driver.page_source
        driver.save_screenshot("screenshots/menu_vacio.png")
    
    def test_agregar_bebida_valida(self, driver):
        """TC02: Agregar bebida válida desde Angular"""
        driver.get("http://localhost:4200")
        
        wait = WebDriverWait(driver, 10)
        
        name_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='input-name']"))
        )
        name_input.clear()
        name_input.send_keys("Cappuccino E2E")
        
        size_select = driver.find_element(By.CSS_SELECTOR, "[data-testid='select-size']")
        size_select.send_keys("large")
        
        price_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='input-price']")
        price_input.clear()
        price_input.send_keys("4.50")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='btn-submit']")
        submit_btn.click()
        
        success_msg = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "exitosamente" in success_msg.text
        
        driver.save_screenshot("screenshots/bebida_agregada.png")
        time.sleep(2)
    
    def test_validacion_nombre_vacio(self, driver):
        """Test: Validar que no se puede enviar nombre vacío"""
        driver.get("http://localhost:4200")
        
        wait = WebDriverWait(driver, 10)
        
        price_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='input-price']"))
        )
        price_input.send_keys("3.00")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='btn-submit']")
        
        assert not submit_btn.is_enabled()
        
        driver.save_screenshot("screenshots/validacion_nombre.png")