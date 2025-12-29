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
    Fixture to navigate to the Market99 home page and return a HomePage object.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_page_down_action_grid(driver, home_page):
    """
    Test Case: PRES-40 - Verify page scroll down via Selenium Grid on multiple browsers.
    Steps:
      1. Start remote browser via Grid.
      2. Navigate to https://market99.com/.
      3. Call home_page.page_down().
      4. Wait 2 seconds.
      5. Close session.
    Expected Result:
      - Page scroll down executes without exceptions.
      - Page remains responsive after scrolling.
    """
    # Action: Scroll down the page
    home_page.page_down()
    time.sleep(2)

    # Assertion: Check page is still responsive by verifying page title is accessible
    assert driver.title is not None and len(driver.title) > 0, "Page should remain responsive after scrolling down"

    # Additional assertion: No exceptions should be raised during scroll
    # (pytest will fail the test if any exception occurs)

    # Teardown handled by fixture

# End of test script
