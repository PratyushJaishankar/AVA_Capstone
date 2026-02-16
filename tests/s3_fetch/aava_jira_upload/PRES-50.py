import pytest
import time
from page_objects.home_page import HomePage
from utils.browser_config import get_browsers

# Get list of browsers to test on (from project utility)
browsers = get_browsers()

@pytest.fixture
def home_page(driver):
    """
    Fixture to initialize HomePage object after navigating to the site.
    """
    driver.get("https://market99.com/")
    return HomePage(driver)

@pytest.mark.parametrize("driver", browsers, indirect=True)
def test_scroll_to_top(driver, home_page):
    """
    Test Case: PRES-50
    Purpose: Verify that calling home_page.scroll_to_top() scrolls the page to the top without exceptions.
    Steps:
        1. Start browser.
        2. Navigate to https://market99.com/.
        3. Call home_page.scroll_to_top().
        4. Wait 2s.
        5. End session.
    Expected Result: Page scrolls to top; no exceptions.
    Test Type: Functional
    """
    # Action: Scroll to top of the page
    try:
        home_page.scroll_to_top()
        time.sleep(2)
    except Exception as e:
        pytest.fail(f"Exception occurred while scrolling to top: {e}")

    # Assertion: No exceptions should occur, and optionally verify scroll position
    # If HomePage exposes a method to get scroll position, use it here.
    # Example (if implemented):
    # assert home_page.get_scroll_position() == 0, "Page should be scrolled to the top"
