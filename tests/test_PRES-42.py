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
    Pytest fixture to initialize a remote browser session via Selenium Grid.
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
def test_scroll_to_top_no_exceptions(driver, home_page):
    """
    Test Case: Verify page scrolls to top using home_page.scroll_to_top() via Selenium Grid.
    Steps:
      1. Start remote browser via Grid.
      2. Navigate to https://market99.com/.
      3. Call home_page.scroll_to_top().
      4. Wait 2s.
      5. Close session.
    Expected Result: Page scrolls to the top; no exceptions.
    """
    # Scroll to top of the page
    try:
        home_page.scroll_to_top()
        time.sleep(2)
        # Optionally, verify scroll position is at the top
        scroll_position = driver.execute_script("return window.pageYOffset;")
        assert scroll_position == 0, "Page should be scrolled to the top (Y offset = 0)"
    except Exception as e:
        pytest.fail(f"Exception occurred during scroll_to_top: {e}")
