"""
=============================================================================
E2E Testing Configuration for VirtualCoffee
Centralized configuration for Selenium WebDriver and test settings
=============================================================================
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

@dataclass
class ApplicationUrls:
    """URLs for VirtualCoffee applications"""
    angular_ui: str = "http://localhost:4200"
    react_ui: str = "http://localhost:3000"
    java_api: str = "http://localhost:8080"
    python_api: str = "http://localhost:8000"

@dataclass
class TestConfig:
    """Main test configuration class"""
    
    # Application URLs  
    urls: ApplicationUrls = field(default_factory=ApplicationUrls)
    
    # Browser settings
    browser: str = "chrome"  # chrome, firefox, edge
    headless: bool = True
    window_size: tuple = (1920, 1080)
    implicit_wait: int = 10
    explicit_wait: int = 15
    page_load_timeout: int = 30
    
    # Screenshot settings
    screenshot_on_failure: bool = True
    screenshot_dir: str = "screenshots"
    
    # Test execution settings
    parallel_workers: int = 4
    retry_count: int = 3
    test_timeout: int = 300
    
    # Selenium Grid settings (for parallel execution)
    use_selenium_grid: bool = False
    grid_hub_url: str = "http://localhost:4444/wd/hub"
    
    # Environment settings
    environment: str = os.getenv("TEST_ENVIRONMENT", "local")
    ci_mode: bool = os.getenv("CI", "false").lower() == "true"
    
    def __post_init__(self):
        """Post-initialization adjustments based on environment"""
        if self.ci_mode:
            self.headless = True
            self.screenshot_on_failure = True
            self.retry_count = 1
        
        # Override URLs if environment variables are set
        if os.getenv("ANGULAR_URL"):
            self.urls.angular_ui = os.getenv("ANGULAR_URL")
        if os.getenv("REACT_URL"):
            self.urls.react_ui = os.getenv("REACT_URL")
        if os.getenv("JAVA_API_URL"):
            self.urls.java_api = os.getenv("JAVA_API_URL")
        if os.getenv("PYTHON_API_URL"):
            self.urls.python_api = os.getenv("PYTHON_API_URL")
            
        # Override browser if environment variable is set
        if os.getenv("BROWSER"):
            self.browser = os.getenv("BROWSER").lower()
            
        # Override headless mode if environment variable is set
        if os.getenv("HEADLESS"):
            self.headless = os.getenv("HEADLESS").lower() == "true"

class WebDriverFactory:
    """Factory for creating WebDriver instances with proper configuration"""
    
    def __init__(self, config: TestConfig):
        self.config = config
    
    def create_chrome_driver(self) -> webdriver.Chrome:
        """Create configured Chrome WebDriver"""
        options = ChromeOptions()
        
        # Basic options
        if self.config.headless:
            options.add_argument('--headless')
        
        # Security and stability options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript-harmony-shipping')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        
        # Window size
        options.add_argument(f'--window-size={self.config.window_size[0]},{self.config.window_size[1]}')
        
        # Performance optimizations
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-sync')
        options.add_argument('--disable-translate')
        options.add_argument('--disable-web-resources')
        options.add_argument('--hide-scrollbars')
        options.add_argument('--metrics-recording-only')
        options.add_argument('--mute-audio')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--no-first-run')
        
        # CI-specific options
        if self.config.ci_mode:
            options.add_argument('--disable-logging')
            options.add_argument('--disable-gl-drawing-for-tests')
            options.add_argument('--disable-gl-extensions')
        
        # Selenium Grid configuration
        if self.config.use_selenium_grid:
            driver = webdriver.Remote(
                command_executor=self.config.grid_hub_url,
                options=options
            )
        else:
            service = webdriver.ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        
        # Configure timeouts
        driver.implicitly_wait(self.config.implicit_wait)
        driver.set_page_load_timeout(self.config.page_load_timeout)
        
        return driver
    
    def create_firefox_driver(self) -> webdriver.Firefox:
        """Create configured Firefox WebDriver"""
        options = FirefoxOptions()
        
        # Basic options
        if self.config.headless:
            options.add_argument('--headless')
        
        # Window size
        options.add_argument(f'--width={self.config.window_size[0]}')
        options.add_argument(f'--height={self.config.window_size[1]}')
        
        # Performance options
        options.set_preference("browser.cache.disk.enable", False)
        options.set_preference("browser.cache.memory.enable", False)
        options.set_preference("browser.cache.offline.enable", False)
        options.set_preference("network.http.use-cache", False)
        
        # Selenium Grid configuration
        if self.config.use_selenium_grid:
            driver = webdriver.Remote(
                command_executor=self.config.grid_hub_url,
                options=options
            )
        else:
            service = webdriver.FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
        
        # Configure timeouts
        driver.implicitly_wait(self.config.implicit_wait)
        driver.set_page_load_timeout(self.config.page_load_timeout)
        
        return driver
    
    def create_driver(self) -> webdriver.Remote:
        """Create WebDriver based on configuration"""
        if self.config.browser.lower() == "chrome":
            return self.create_chrome_driver()
        elif self.config.browser.lower() == "firefox":
            return self.create_firefox_driver()
        else:
            raise ValueError(f"Unsupported browser: {self.config.browser}")

class TestSelectors:
    """Centralized test selectors for VirtualCoffee applications"""
    
    # Angular UI selectors (ui-bebidas)
    ANGULAR = {
        "input_name": "[data-testid='input-name']",
        "select_size": "[data-testid='select-size']", 
        "input_price": "[data-testid='input-price']",
        "btn_submit": "[data-testid='btn-submit']",
        "success_message": ".success-message",
        "menu_table": ".menu-table",
        "menu_container": ".menu-container"
    }
    
    # React UI selectors (ui-pedidos)
    REACT = {
        "input_drink_name": "[data-testid='input-drink-name']",
        "select_size": "[data-testid='select-size']",
        "btn_submit": "[data-testid='btn-submit']", 
        "success_message": "[data-testid='success-message']",
        "orders_table": "[data-testid='orders-table']",
        "order_history": "[data-testid='order-history']"
    }

class TestData:
    """Test data for VirtualCoffee E2E tests"""
    
    BEVERAGES = [
        {"name": "Cappuccino E2E", "size": "large", "price": "4.50"},
        {"name": "Latte Test", "size": "medium", "price": "3.75"}, 
        {"name": "Espresso Auto", "size": "small", "price": "2.50"},
        {"name": "Mocha E2E", "size": "large", "price": "5.00"},
        {"name": "Americano Test", "size": "medium", "price": "3.25"}
    ]
    
    SIZES = ["small", "medium", "large"]
    
    INVALID_DATA = {
        "empty_name": {"name": "", "size": "medium", "price": "3.00"},
        "negative_price": {"name": "Test Drink", "size": "large", "price": "-1.00"},
        "invalid_size": {"name": "Test Drink", "size": "jumbo", "price": "4.00"}
    }

# Global configuration instance
config = TestConfig()
driver_factory = WebDriverFactory(config)
selectors = TestSelectors()
test_data = TestData()

# Utility functions
def get_test_config() -> TestConfig:
    """Get the global test configuration"""
    return config

def create_webdriver() -> webdriver.Remote:
    """Create a WebDriver instance using global configuration"""
    return driver_factory.create_driver()

def get_selectors() -> TestSelectors:
    """Get the centralized selectors"""
    return selectors

def get_test_data() -> TestData:
    """Get the test data"""
    return test_data

def setup_test_directories():
    """Create necessary test directories"""
    import os
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("reports", exist_ok=True) 
    os.makedirs("allure-results", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("coverage", exist_ok=True)

if __name__ == "__main__":
    # Print configuration for debugging
    print("VirtualCoffee E2E Test Configuration:")
    print(f"Environment: {config.environment}")
    print(f"Browser: {config.browser}")
    print(f"Headless: {config.headless}")
    print(f"Angular UI: {config.urls.angular_ui}")
    print(f"React UI: {config.urls.react_ui}")
    print(f"Java API: {config.urls.java_api}")
    print(f"Python API: {config.urls.python_api}")