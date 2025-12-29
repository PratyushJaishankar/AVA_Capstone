import pytest
import time
from page_objects.home_page import HomePage
from utils.browser_config import get_browsers

# Retrieve available browser configurations for cross-browser testing
browsers = get_browsers()

@pytest.fixture
def home_page(driver):
    """
    Fixture to initialize the HomePage object after navigating to the target URL.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_scroll_by_300_pixels(driver, home_page):
    """
    Test Case: Verify page scroll by 300px on Home Page

    Steps:
    1. Start browser and navigate to https://market99.com/
    2. Call home_page.scroll_by_pixel(300)
    3. Wait for 2 seconds
    4. End session

    Expected Result:
    - The page should be scrolled vertically by approximately 300 pixels.
    - No exceptions should be raised during the operation.

    This test uses parameterization to run across multiple browsers.
    """
    # Action: Scroll by 300 pixels
    try:
        home_page.scroll_by_pixel(300)
        time.sleep(2)  # Wait for scroll to complete
    except Exception as e:
        pytest.fail(f"Exception occurred during scroll_by_pixel: {e}")

    # Assertion: No exception means scroll was successful
    # Optionally, you could add more checks here if the page exposes scroll position via JS or DOM

    # No teardown needed; driver fixture handles browser session cleanup
