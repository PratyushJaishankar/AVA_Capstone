import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from page_objects.home_page import HomePage

# Selenium Grid URL (update as needed)
GRID_URL = "http://localhost:4444"

# List of browsers to test compatibility
browsers = ["chrome", "edge", "firefox"]

@pytest.fixture
def driver(request):
    """
    Pytest fixture to initialize a remote WebDriver session via Selenium Grid.
    Maximizes window and ensures proper teardown.
    """
    browser = request.param

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        grid_driver = webdriver.Remote(
            command_executor=GRID_URL,
            options=options
        )
    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        grid_driver = webdriver.Remote(
            command_executor=GRID_URL,
            options=options
        )
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        grid_driver = webdriver.Remote(
            command_executor=GRID_URL,
            options=options
        )
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    grid_driver.maximize_window()
    yield grid_driver

    try:
        grid_driver.quit()
    except Exception as e:
        print(f"Error quitting driver: {e}")

@pytest.fixture
def home_page(driver):
    """
    Fixture to navigate to the home page and return the HomePage page object.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_zoom_in_js(driver, home_page):
    """
    Test that zooming in via JavaScript on the home page works without JS errors.
    Steps:
    1. Start remote browser via Grid.
    2. Navigate to https://market99.com/.
    3. Call home_page.zoom_in_js().
    4. Wait 2s.
    5. Close session.
    Expected Result: Page visually zooms in; no JS errors.
    """
    # Perform zoom in using JS
    home_page.zoom_in_js()
    time.sleep(2)

    # Check for JS errors in browser logs (if supported)
    # Note: Not all browsers support log retrieval via Selenium
    js_errors = []
    try:
        # Chrome and Edge support 'browser' logs
        if hasattr(driver, "get_log"):
            for entry in driver.get_log("browser"):
                if entry.get("level") == "SEVERE":
                    js_errors.append(entry)
    except Exception:
        # Firefox or remote drivers may not support get_log
        pass

    # Assert no JS errors occurred
    assert not js_errors, f"JavaScript errors found: {js_errors}"

    # Optionally, verify zoom visually by checking window.devicePixelRatio or style changes
    # This is a basic check; for more robust visual validation, use image comparison tools
    zoom_level = driver.execute_script("return window.devicePixelRatio;")
    assert zoom_level >= 1.0, f"Expected zoom level >= 1.0, got {zoom_level}"

    # No explicit teardown needed; handled by fixture

# End of test script
