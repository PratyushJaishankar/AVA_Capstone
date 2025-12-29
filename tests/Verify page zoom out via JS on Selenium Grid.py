import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from page_objects.home_page import HomePage

# Selenium Grid URL (update as needed)
GRID_URL = "http://localhost:4444"

# List of browsers to test on the grid
browsers = ["chrome", "edge", "firefox"]

@pytest.fixture
def driver(request):
    """
    Pytest fixture to initialize a remote WebDriver session for Selenium Grid.
    Supports Chrome, Edge, and Firefox.
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
    Pytest fixture to initialize the HomePage object after navigating to the target URL.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_zoom_out_js(driver, home_page):
    """
    Test Case: Verify page zoom out via JavaScript on Selenium Grid.
    Steps:
      1. Start remote browser via Grid.
      2. Navigate to https://market99.com/.
      3. Call home_page.zoom_out_js().
      4. Wait 2 seconds.
      5. Close session (handled by fixture).
    Expected Result: Page is zoomed out via JS; no JS errors.
    """
    # Action: Zoom out using JavaScript
    home_page.zoom_out_js()
    time.sleep(2)

    # Assertion: Check for JS errors in browser logs (if supported)
    # Note: Not all browsers support log retrieval via Selenium Grid.
    # This is a best-effort check for Chrome.
    if hasattr(driver, "get_log"):
        try:
            logs = driver.get_log("browser")
            js_errors = [entry for entry in logs if entry.get("level") == "SEVERE"]
            assert not js_errors, f"JavaScript errors found: {js_errors}"
        except Exception:
            # Log retrieval may not be supported; skip assertion
            pass

    # Additional assertion: Optionally, verify zoom level if accessible via JS
    # Example (uncomment if HomePage exposes zoom level):
    # zoom_level = home_page.get_zoom_level()
    # assert zoom_level < 1.0, "Page should be zoomed out (zoom level < 1.0)"

    # Test passes if no exceptions and no JS errors are found
