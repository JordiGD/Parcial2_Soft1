"""
Pytest configuration and shared fixtures for VirtualCoffee E2E tests
"""

import pytest
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from config import get_test_config, setup_test_directories

# Setup test directories at module load
setup_test_directories()

@pytest.fixture(scope="session")
def test_config():
    """Get test configuration"""
    return get_test_config()

@pytest.fixture(scope="class")  
def driver(test_config):
    """Create WebDriver instance for test class"""
    options = ChromeOptions()
    
    # Configure Chrome options based on environment
    if test_config.headless:
        options.add_argument('--headless')
    
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(f'--window-size={test_config.window_size[0]},{test_config.window_size[1]}')
    
    # Additional options for stability
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    
    # Create driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Configure timeouts
    driver.implicitly_wait(test_config.implicit_wait)
    driver.set_page_load_timeout(test_config.page_load_timeout)
    
    yield driver
    
    # Cleanup
    driver.quit()

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    """Automatically take screenshot on test failure"""
    yield
    
    if request.node.rep_call.failed:
        # Generate screenshot filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name.replace("::", "_").replace(" ", "_")
        filename = f"screenshots/failure_{test_name}_{timestamp}.png"
        
        try:
            driver.save_screenshot(filename)
            print(f"Screenshot saved: {filename}")
        except Exception as e:
            print(f"Failed to save screenshot: {e}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot fixture"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture
def application_urls(test_config):
    """Get application URLs"""
    return test_config.urls

@pytest.fixture
def wait_time():
    """Standard wait time for tests"""
    return 2

def pytest_configure(config):
    """Configure pytest"""
    # Add custom markers
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    
def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Add smoke marker to specific tests
    for item in items:
        if "complete_flow" in item.name:
            item.add_marker(pytest.mark.smoke)
        if "angular" in item.name or "react" in item.name:
            item.add_marker(pytest.mark.regression)

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment"""
    print("\nSetting up E2E test environment...")
    
    # Ensure directories exist
    setup_test_directories()
    
    # Print configuration
    config = get_test_config()
    print(f"Browser: {config.browser}")
    print(f"Headless: {config.headless}")
    print(f"Angular URL: {config.urls.angular_ui}")
    print(f"React URL: {config.urls.react_ui}")
    
    yield
    
    print("\nE2E test environment cleanup complete.")

class TestUtils:
    """Utility methods for tests"""
    
    @staticmethod
    def generate_unique_name(prefix="Test"):
        """Generate unique name with timestamp"""
        return f"{prefix}_{int(time.time())}"
    
    @staticmethod
    def wait_and_screenshot(driver, filename_prefix):
        """Wait and take screenshot"""
        time.sleep(2)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{filename_prefix}_{timestamp}.png"
        driver.save_screenshot(filename)
        return filename

@pytest.fixture
def test_utils():
    """Get test utilities"""
    return TestUtils()