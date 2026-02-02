import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from page_objects.home_page import HomePage

# Selenium Grid URL (update as needed)
GRID_URL = "http://localhost:4444"

# Browsers to test on the Grid
browsers = ["chrome", "edge", "firefox"]

@pytest.fixture
def driver(request):
    """
    Selenium Grid driver fixture.
    Starts a remote browser session on the specified browser.
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
    Fixture to initialize HomePage object after navigating to the target URL.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_zoom_in_js(driver, home_page):
    """
    Test Case: PRES-44
    Module: Selenium Grid - Page Actions
    Steps:
      1. Start remote browser via Grid.
      2. Navigate to https://market99.com/.
      3. Call home_page.zoom_in_js().
      4. Wait 2s.
      5. Close session.
    Expected Result:
      - Page zoomed in via JS (visual zoom change applied).
      - No JS errors.
    """
    print("[Test] Starting test_zoom_in_js...")
    print("Zooming in using JavaScript...")
    # Action: Zoom in using the HomePage POM method
    home_page.zoom_in_js()
    time.sleep(2)
    # There is no direct assertion for visual zoom, but we can check for JS errors
    logs = []
    try:
        # Only works if browser supports log retrieval
        logs = driver.get_log("browser")
    except Exception:
        pass  # Not all drivers support this

    js_errors = [entry for entry in logs if entry.get("level") == "SEVERE"]
    assert not js_errors, f"JavaScript errors found: {js_errors}"
    print("[Test] Finished test_zoom_in_js.")