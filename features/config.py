"""
BDD Configuration for VirtualCoffee Features Testing
Centralized configuration for Behave testing environment
"""
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path


@dataclass
class BrowserConfig:
    """Browser configuration for BDD testing"""
    name: str = "chrome"
    headless: bool = True
    window_size: str = "1920,1080"
    implicit_wait: int = 10
    page_load_timeout: int = 30
    options: List[str] = field(default_factory=lambda: [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-images"
    ])


@dataclass
class ApplicationUrls:
    """Application URLs for testing"""
    api_bebidas: str = "http://localhost:8000"
    api_pedidos: str = "http://localhost:8080"
    ui_angular: str = "http://localhost:4200"
    ui_react: str = "http://localhost:3000"
    selenium_grid: Optional[str] = None


@dataclass
class TestConfig:
    """Main test configuration"""
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    urls: ApplicationUrls = field(default_factory=ApplicationUrls)
    screenshots_dir: str = "screenshots"
    reports_dir: str = "reports"
    allure_results_dir: str = "allure-results"
    timeout: int = 30
    retry_count: int = 3
    parallel_workers: int = 1
    tags: List[str] = field(default_factory=list)
    environment: str = "development"


def get_test_config() -> TestConfig:
    """
    Get test configuration from environment variables or defaults
    """
    config = TestConfig()
    
    # Browser configuration from environment
    if os.getenv("BROWSER_NAME"):
        config.browser.name = os.getenv("BROWSER_NAME", "chrome")
    
    if os.getenv("HEADLESS"):
        config.browser.headless = os.getenv("HEADLESS", "true").lower() == "true"
    
    # Application URLs from environment (Docker support)
    if os.getenv("API_BEBIDAS_URL"):
        config.urls.api_bebidas = os.getenv("API_BEBIDAS_URL")
    
    if os.getenv("API_PEDIDOS_URL"):
        config.urls.api_pedidos = os.getenv("API_PEDIDOS_URL")
    
    if os.getenv("UI_ANGULAR_URL"):
        config.urls.ui_angular = os.getenv("UI_ANGULAR_URL")
    
    if os.getenv("UI_REACT_URL"):
        config.urls.ui_react = os.getenv("UI_REACT_URL")
    
    if os.getenv("SELENIUM_GRID_URL"):
        config.urls.selenium_grid = os.getenv("SELENIUM_GRID_URL")
    
    # Test environment configuration
    if os.getenv("TEST_ENVIRONMENT"):
        config.environment = os.getenv("TEST_ENVIRONMENT", "development")
    
    if os.getenv("PARALLEL_WORKERS"):
        config.parallel_workers = int(os.getenv("PARALLEL_WORKERS", "1"))
    
    # CI/CD specific configurations
    if os.getenv("CI") == "true":
        config.browser.headless = True
        config.browser.options.extend([
            "--remote-debugging-port=9222",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-renderer-backgrounding"
        ])
    
    # Create directories if they don't exist
    Path(config.screenshots_dir).mkdir(exist_ok=True)
    Path(config.reports_dir).mkdir(exist_ok=True)
    Path(config.allure_results_dir).mkdir(exist_ok=True)
    
    return config


# Global configuration instance
TEST_CONFIG = get_test_config()


class FeatureConfig:
    """Feature-specific configuration and utilities"""
    
    @staticmethod
    def get_api_base_urls() -> Dict[str, str]:
        """Get API base URLs for different services"""
        return {
            "bebidas": TEST_CONFIG.urls.api_bebidas,
            "pedidos": TEST_CONFIG.urls.api_pedidos
        }
    
    @staticmethod
    def get_ui_urls() -> Dict[str, str]:
        """Get UI URLs for different applications"""
        return {
            "angular": TEST_CONFIG.urls.ui_angular,
            "react": TEST_CONFIG.urls.ui_react
        }
    
    @staticmethod
    def get_test_data() -> Dict[str, any]:
        """Get test data for BDD scenarios"""
        return {
            "bebidas": {
                "latte": {"name": "Latte", "sizes": ["small", "medium", "large"], "prices": {"small": 2.50, "medium": 3.50, "large": 4.50}},
                "cappuccino": {"name": "Cappuccino", "sizes": ["medium", "large"], "prices": {"medium": 3.00, "large": 4.00}},
                "americano": {"name": "Americano", "sizes": ["small", "medium"], "prices": {"small": 2.00, "medium": 2.50}},
                "espresso": {"name": "Espresso", "sizes": ["small"], "prices": {"small": 1.50}},
                "mocha": {"name": "Mocha", "sizes": ["small", "medium", "large"], "prices": {"small": 3.00, "medium": 4.00, "large": 5.00}}
            },
            "invalid_bebidas": ["SuperCafe", "MegaLatte", "UltraCappuccino"],
            "estados_pedido": ["PENDING", "CONFIRMED", "PREPARING", "READY", "DELIVERED", "CANCELLED", "REJECTED"]
        }


# Export configuration objects
__all__ = [
    "TestConfig",
    "BrowserConfig", 
    "ApplicationUrls",
    "FeatureConfig",
    "get_test_config",
    "TEST_CONFIG"
]