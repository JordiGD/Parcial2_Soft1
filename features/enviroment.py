"""
Behave environment setup for VirtualCoffee BDD testing
Configures browser, test data, and cleanup procedures
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config import get_test_config, FeatureConfig
import os
import json
import logging
from datetime import datetime
from pathlib import Path


def setup_logging():
    """Setup logging for BDD tests"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/bdd_tests_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def create_driver(config) -> WebDriver:
    """Create WebDriver instance based on configuration"""
    if config.browser.name.lower() == "chrome":
        options = webdriver.ChromeOptions()
        if config.browser.headless:
            options.add_argument('--headless')
        
        # Add all configured options
        for option in config.browser.options:
            options.add_argument(option)
        
        options.add_argument(f'--window-size={config.browser.window_size}')
        
        # Use Selenium Grid if configured
        if config.urls.selenium_grid:
            driver = webdriver.Remote(
                command_executor=config.urls.selenium_grid,
                options=options
            )
        else:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
    
    elif config.browser.name.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        if config.browser.headless:
            options.add_argument('--headless')
        
        # Use Selenium Grid if configured
        if config.urls.selenium_grid:
            driver = webdriver.Remote(
                command_executor=config.urls.selenium_grid,
                options=options
            )
        else:
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
    
    else:
        raise ValueError(f"Unsupported browser: {config.browser.name}")
    
    driver.implicitly_wait(config.browser.implicit_wait)
    driver.set_page_load_timeout(config.browser.page_load_timeout)
    
    return driver


def before_all(context):
    """Setup antes de todas las features"""
    # Setup logging
    context.logger = setup_logging()
    context.logger.info("Iniciando ejecución de pruebas BDD")
    
    # Load configuration
    context.config = get_test_config()
    context.feature_config = FeatureConfig()
    
    # Create directories
    os.makedirs(context.config.screenshots_dir, exist_ok=True)
    os.makedirs(context.config.reports_dir, exist_ok=True)
    os.makedirs(context.config.allure_results_dir, exist_ok=True)
    
    # Store configuration paths
    context.screenshots_dir = context.config.screenshots_dir
    context.reports_dir = context.config.reports_dir
    
    # Initialize test statistics
    context.test_stats = {
        "scenarios_total": 0,
        "scenarios_passed": 0,
        "scenarios_failed": 0,
        "features_total": 0,
        "start_time": datetime.now()
    }
    
    # Store URLs and test data for easy access
    context.api_urls = context.feature_config.get_api_base_urls()
    context.ui_urls = context.feature_config.get_ui_urls()
    context.test_data = context.feature_config.get_test_data()
    
    context.logger.info(f"Configuración cargada - Browser: {context.config.browser.name}, Environment: {context.config.environment}")


def before_feature(context, feature):
    """Setup antes de cada feature"""
    context.test_stats["features_total"] += 1
    context.logger.info(f"Ejecutando feature: {feature.name}")


def before_scenario(context, scenario):
    """Setup antes de cada escenario"""
    context.test_stats["scenarios_total"] += 1
    context.logger.info(f"Ejecutando escenario: {scenario.name}")
    
    # Create driver for each scenario
    try:
        context.driver = create_driver(context.config)
        context.scenario_start_time = datetime.now()
    except Exception as e:
        context.logger.error(f"Error creando driver: {str(e)}")
        raise


def after_scenario(context, scenario):
    """Cleanup después de cada escenario"""
    # Update statistics
    if scenario.status == "passed":
        context.test_stats["scenarios_passed"] += 1
    else:
        context.test_stats["scenarios_failed"] += 1
    
    # Take screenshot
    if hasattr(context, 'driver'):
        try:
            # Create screenshot filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            scenario_name = scenario.name.replace(' ', '_').replace('/', '_').lower()
            screenshot_name = f"{scenario_name}_{timestamp}_{scenario.status}"
            screenshot_path = f'{context.screenshots_dir}/{screenshot_name}.png'
            
            # Save screenshot
            context.driver.save_screenshot(screenshot_path)
            context.logger.info(f"Screenshot guardada: {screenshot_path}")
            
            # Save page source for failed scenarios
            if scenario.status == "failed":
                source_path = f'{context.screenshots_dir}/{screenshot_name}_source.html'
                with open(source_path, 'w', encoding='utf-8') as f:
                    f.write(context.driver.page_source)
                context.logger.info(f"Page source guardado: {source_path}")
            
        except Exception as e:
            context.logger.warning(f"Error guardando screenshot: {str(e)}")
        
        finally:
            # Always quit driver
            try:
                context.driver.quit()
            except Exception as e:
                context.logger.warning(f"Error cerrando driver: {str(e)}")
    
    # Log scenario completion
    execution_time = (datetime.now() - context.scenario_start_time).total_seconds()
    context.logger.info(f"Escenario completado: {scenario.name} - Status: {scenario.status} - Tiempo: {execution_time:.2f}s")


def after_feature(context, feature):
    """Cleanup después de cada feature"""
    context.logger.info(f"Feature completada: {feature.name}")


def after_all(context):
    """Cleanup después de todas las features"""
    # Calculate final statistics
    end_time = datetime.now()
    total_time = (end_time - context.test_stats["start_time"]).total_seconds()
    
    # Generate summary report
    summary = {
        "execution_summary": {
            "start_time": context.test_stats["start_time"].isoformat(),
            "end_time": end_time.isoformat(),
            "total_execution_time_seconds": total_time,
            "features_executed": context.test_stats["features_total"],
            "scenarios_total": context.test_stats["scenarios_total"],
            "scenarios_passed": context.test_stats["scenarios_passed"],
            "scenarios_failed": context.test_stats["scenarios_failed"],
            "success_rate_percentage": (context.test_stats["scenarios_passed"] / context.test_stats["scenarios_total"] * 100) if context.test_stats["scenarios_total"] > 0 else 0
        },
        "configuration": {
            "browser": context.config.browser.name,
            "environment": context.config.environment,
            "headless": context.config.browser.headless,
            "parallel_workers": context.config.parallel_workers
        },
        "urls_tested": {
            "api_endpoints": context.api_urls,
            "ui_applications": context.ui_urls
        }
    }
    
    # Save summary to JSON
    summary_path = f"{context.reports_dir}/execution_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Log final results
    context.logger.info("=" * 60)
    context.logger.info("RESUMEN DE EJECUCIÓN BDD")
    context.logger.info("=" * 60)
    context.logger.info(f"Features ejecutadas: {context.test_stats['features_total']}")
    context.logger.info(f"Escenarios totales: {context.test_stats['scenarios_total']}")
    context.logger.info(f"Escenarios exitosos: {context.test_stats['scenarios_passed']}")
    context.logger.info(f"Escenarios fallidos: {context.test_stats['scenarios_failed']}")
    context.logger.info(f"Tasa de éxito: {summary['execution_summary']['success_rate_percentage']:.1f}%")
    context.logger.info(f"Tiempo total: {total_time:.2f} segundos")
    context.logger.info(f"Resumen guardado en: {summary_path}")
    context.logger.info("=" * 60)