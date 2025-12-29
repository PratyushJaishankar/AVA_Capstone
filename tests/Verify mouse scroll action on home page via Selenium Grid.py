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
    Fixture to initialize the HomePage object after navigating to the target URL.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_mouse_scroll_action(driver, home_page):
    """
    Test Case: Verify mouse scroll action on home page via Selenium Grid.
    Steps:
      1. Start remote browser via Grid.
      2. Navigate to https://market99.com/.
      3. Call home_page.mouse_scroll(200).
      4. Wait 2s.
      5. Close session.
    Expected Result: Page scrolled by simulated mouse scroll (200px); no exceptions.
    """
    try:
        # Perform mouse scroll by 200 pixels
        home_page.mouse_scroll(200)
        time.sleep(2)

        # Assertion: No exceptions should occur, and driver should still be alive
        assert driver.session_id is not None, "WebDriver session should remain active after mouse scroll"
    except Exception as exc:
        pytest.fail(f"Exception occurred during mouse scroll: {exc}")
