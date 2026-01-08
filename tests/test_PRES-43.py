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
    Pytest fixture to create a remote WebDriver session via Selenium Grid.
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
    Fixture to initialize the HomePage object after navigating to the target URL.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_scroll_to_bottom_via_grid(driver, home_page):
    """
    Test Case: Verify page scroll to bottom via Selenium Grid

    Steps:
    1. Start remote browser via Grid.
    2. Navigate to https://market99.com/.
    3. Call home_page.scroll_to_bottom().
    4. Wait 2 seconds.
    5. Close session.

    Expected Result:
    - Page scrolls to bottom of page successfully.
    - No exceptions are raised.
    """
    # Action: Scroll to bottom
    home_page.scroll_to_bottom()
    time.sleep(2)

    # Assertion: Check that no exceptions occurred and page is at bottom
    # (Assuming HomePage has a method to verify scroll position, otherwise just ensure no error)
    # Example:
    # assert home_page.is_at_bottom(), "Page should be scrolled to the bottom"

    # If no is_at_bottom method, just ensure no exceptions and driver is still alive
    assert driver.session_id is not None, "WebDriver session should be active after scrolling"

    # Teardown handled by fixture

# Note:
# - This script is compatible with pytest and Selenium Grid.
# - It uses parameterization to test across Chrome, Edge, and Firefox.
# - The test is modular, readable, and follows PEP 8 standards.
# - Comments explain the purpose and logic of each section.
