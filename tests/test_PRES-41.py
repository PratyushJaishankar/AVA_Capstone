import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from page_objects.home_page import HomePage

# Selenium Grid URL (update as needed for your environment)
GRID_URL = "http://localhost:4444"

# List of browsers to test compatibility
browsers = ["chrome", "edge", "firefox"]

@pytest.fixture
def driver(request):
    """
    Pytest fixture to create a remote WebDriver session via Selenium Grid.
    Maximizes the window and ensures proper teardown.
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
    Pytest fixture to instantiate the HomePage object after navigating to the target URL.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_scroll_by_pixel_300(driver, home_page):
    """
    Test Case: PRES-41 - Verify page scrolls by ~300 pixels using home_page.scroll_by_pixel(300)
    Steps:
      1. Start remote browser via Selenium Grid.
      2. Navigate to https://market99.com/.
      3. Call home_page.scroll_by_pixel(300).
      4. Wait 2 seconds.
      5. Close session.
    Expected Result: Page is scrolled by ~300 pixels; no errors thrown.
    Test Type: Compatibility/Functional
    """
    initial_scroll = driver.execute_script("return window.pageYOffset;")
    home_page.scroll_by_pixel(300)
    time.sleep(2)
    final_scroll = driver.execute_script("return window.pageYOffset;")
    # Assert that the page has scrolled by approximately 300 pixels
    assert abs(final_scroll - initial_scroll - 300) < 20, (
        f"Expected scroll by ~300 pixels, but got {final_scroll - initial_scroll} pixels"
    )
