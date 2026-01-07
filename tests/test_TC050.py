import pytest
import time
from page_objects.home_page import HomePage
from utils.browser_config import get_browsers

# Retrieve all available browser drivers for cross-browser testing
browsers = get_browsers()

@pytest.fixture
def home_page(driver):
    """
    Fixture to initialize the HomePage object after navigating to the target URL.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_scroll_to_top(driver, home_page):
    """
    Test to verify that the scroll_to_top() method scrolls the page to the top without exceptions.

    Steps:
    1. Start browser and navigate to https://market99.com/
    2. Call home_page.scroll_to_top()
    3. Wait for 2 seconds
    4. End session

    Expected Result:
    - Page scrolls to the top.
    - No exceptions are raised.
    """
    # Scroll down first to ensure the page is not already at the top
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Action: Scroll to top using the method under test
    try:
        home_page.scroll_to_top()
        time.sleep(2)  # Wait for scroll animation/effects

        # Assertion: The page should be at the top (window.scrollY == 0)
        scroll_position = driver.execute_script("return window.scrollY;")
        assert scroll_position == 0, f"Expected scroll position to be 0, got {scroll_position}"

    except Exception as e:
        pytest.fail(f"Exception occurred during scroll_to_top(): {e}")
