import pytest
import time
from page_objects.home_page import HomePage
from utils.browser_config import get_browsers

# Get the list of browsers to test against
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
    Test Case: PRES-50
    Purpose: Verify that calling home_page.scroll_to_top() scrolls the page to the top without exceptions.
    Steps:
        1. Start browser.
        2. Navigate to https://market99.com/.
        3. Call home_page.scroll_to_top().
        4. Wait 2 seconds.
        5. End session.
    Expected Result: Page scrolls to top; no exceptions.
    """
    # Action: Scroll to the top of the page
    try:
        home_page.scroll_to_top()
        time.sleep(2)
        # Assertion: No exceptions should occur, and the scroll position should be at the top
        scroll_position = driver.execute_script("return window.pageYOffset;")
        assert scroll_position == 0, "Page should be scrolled to the top (Y offset = 0)"
    except Exception as e:
        pytest.fail(f"Exception occurred during scroll_to_top: {e}")