import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread
import time

from app import app

# Fixture to initialize and quit the WebDriver
@pytest.fixture(scope="module")
def driver():
    """Initializes a headless Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

# Fixture to run the Dash app in a background thread
@pytest.fixture(scope="module")
def dash_app_runner():
    """Runs the Dash app in a separate thread."""
    def run_app():
        app.run_server(debug=False, port=8050)

    thread = Thread(target=run_app)
    thread.daemon = True
    thread.start()
    time.sleep(2) 
    yield

def test_header_is_present(driver, dash_app_runner):
    """
    Tests that the main header "Pink Morsel Sales Analysis" is present.
    """
    driver.get("http://127.0.0.1:8050")
    # Wait for the H1 element to be present
    header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert header.text == "Pink Morsel Sales Analysis"

def test_visualisation_is_present(driver, dash_app_runner):
    """
    Tests that the sales graph component with ID 'sales-graph' is present.
    """
    driver.get("http://127.0.0.1:8050")
    # Wait for the element with ID 'sales-graph' to be present
    graph = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sales-graph"))
    )
    assert graph is not None

def test_region_picker_is_present(driver, dash_app_runner):
    """
    Tests that the region filter radio buttons with ID 'region-filter' are present.
    """
    driver.get("http://127.0.0.1:8050")
    # Wait for the element with ID 'region-filter' to be present
    region_picker = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "region-filter"))
    )
    assert region_picker is not None